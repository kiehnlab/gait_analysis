import pandas as pd
import glob 
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist 
import pdb
from gait_analysis.coordination.tools import videoMetadata
#from coordination.tools import videoMetadata
import argparse
import os
# import seaborn as sns
from scipy.stats import norm
from scipy.signal import find_peaks
from gait_analysis.coordination.coord import iqrMean
#from coordination.coord import iqrMean
from matplotlib.gridspec import GridSpec
from gait_analysis.coordination.sticks import makeStickFigure
from gait_analysis.coordination.constants import *
#from coordination.sticks import makeStickFigure
#from coordination.constants import *

joints = ['hip','knee','ankle','foot']
colors = ['tab:blue','tab:orange','tab:green','tab:red']

def getSwingIdx(peaks,yval,thresh=0.03):
        
    ### Find out ymin in each cycle and pull it to ground 0
    C = len(peaks)
    for i in range(-1,C-1):
        if i == -1:
            lIdx = 0
        else:
            lIdx = peaks[i]
        uIdx = peaks[i+1]
        step = yval[lIdx:uIdx,:]
        yval[lIdx:uIdx,:] = step - step[:,-1].min()
    swing_idx = np.where((yval[:,-1] >= thresh) & (yval[:,-2] >= thresh))[0]
    return swing_idx, yval

def cycleAngles(peaks,angle,num_angles=51):
    C = len(peaks)
    cyc_angle = np.zeros((C-1,num_angles))

    for i in range(C-1):
        lIdx = peaks[i]
        uIdx = peaks[i+1]
        xAxis = np.linspace(lIdx,uIdx,num_angles)
        cyc_angle[i,:] = np.interp(xAxis,np.arange(lIdx,uIdx),angle[lIdx:uIdx])

    return cyc_angle

def pDist(arr):
    N = arr.shape[0]
    d = arr.shape[1]
    dist = np.zeros((N,int(d*(d-1)/2)))

    for i in range(N):
        dist[i] = pdist(arr[i].reshape(-1,1))

    return dist

def smooth(x,L=15):
    M = x.shape[1]
    xF = np.zeros((x.shape[0]-L+1,M))
    for i in range(x.shape[1]):
        xF[:,i] = np.convolve(x[:,i],np.ones((L,))/L,mode='valid')
    return xF

def makeVector(yval,xval,i,j):
    vx = (xval[:,i] - xval[:,j]).reshape(-1,1)
    vy = (yval[:,i] - yval[:,j]).reshape(-1,1)
    v = np.concatenate((vx,vy),axis=1)
    v = v/np.linalg.norm(v,axis=1).reshape(-1,1)
    return v

def measureAngles(yval,xval,i,j,k):
    v1 = makeVector(yval,xval,i,j)
    v2 = makeVector(yval,xval,k,j)
    angle = np.arccos((v1*v2).sum(1))
    return 180*angle/np.pi

def lateral_profiler(data_dir,scale,df):
    # model = 'DLC_resnet50_lateral_analysisOct26shuffle1_100000'
    bodyparts = ['toe','foot','ankle','knee','hip','crest']
    bodyparts = bodyparts[::-1]

    files = sorted(glob.glob(data_dir+'/*.avi'))
    files = [f.split('/')[-1] for f in files]
    data_dir = data_dir.replace('/lateral/','')
    dest = data_dir+'/allProfiles/'
    if not os.path.exists(dest):
        os.mkdir(dest)
    for i in range(len(files)):
        df['name'][i] = files[i].split('.')[0]
    print("Found %d videos to process"%len(files))
    M = len(bodyparts)
    for fName in files:
        meta = videoMetadata(data_dir+'/'+fName)
        data_file = glob.glob(data_dir+'/labels/'+fName.replace('.avi','*.h5'))[0]
        data = pd.read_hdf(data_file)
        N = data.shape[0]
        xval = np.zeros((N,M))
        yval = np.zeros((N,M))
        for m in range(M):
            xval[:,m] = data[model_lateral][bodyparts[m]]['x'].values
            yval[:,m] = data[model_lateral][bodyparts[m]]['y'].values
        # Smooth values
        xval = smooth(xval,L=10)
        yval = smooth(yval,L=10)

        # Rescale x,y to be [0,1]; y per time point, x across
        yval = (1-(yval-yval.min()) / (yval.max()-yval.min()))
        xval = (xval - xval.min(1).reshape(-1,1)) / (xval.max(1)-xval.min(1)).reshape(-1,1)
        t = np.linspace(0,meta['dur'],len(xval))[::-1]
        dist = pDist(xval)
        dist = dist/dist.max()
        xAng = xval * dist.max(1).reshape(-1,1)/scale + t.reshape(-1,1)
        xAng = xAng - (xAng[:,[-1]] - t.reshape(-1,1))

        ### Measure cycles based on foot angle
        peaks, _ = find_peaks(yval[:,-1])
        meanStep = iqrMean(np.diff(peaks))
        ## Remove outlier peaks
        peaks, _ = find_peaks(yval[:,-1],distance=meanStep)
        swing_idx,yval = getSwingIdx(peaks,yval) 
        ### Measure angles
        angles = [measureAngles(yval,xAng,i,i+1,i+2) for i in range(4)]
        cyc_angles = [cycleAngles(peaks,angle) for angle in angles]
        cyc_angles = np.array(cyc_angles)
        ### Check ankle angle for differences
        minAng = cyc_angles.min(2)
        maxAng = cyc_angles.max(2)
        dAng = maxAng-minAng
        dAng[dAng > 120] = 120
        dAng = dAng.mean(1)
        for i in range(len(joints)):
#           df[joints[i]+'_ang'][df.Name in fName] = dAng[i]
            # print(df.at[df.name == fName[9:-4],joints[i]+'_ang'])
            #df.at[df.name == (fName.split('.')[0]),joints[i]+'_ang'] = dAng[i]
            df[df.name == (fName.split('.')[0])][joints[i]+'_ang'] = dAng[i]
        ### Save cycle_angles
        np.save(dest+fName.replace('.avi','.npy'),cyc_angles)
        makeStickFigure(xval,yval,dist,angles,\
                meta['dur'],fName,cyc_angles,peaks,swing_idx,scale,dest)

    return df

def lateral_profiler_combined(data_dir,scale,df):
    # model = 'DLC_resnet50_lateral_analysisOct26shuffle1_100000'
    bodyparts = ['toe','foot','ankle','knee','hip','crest']
    bodyparts = bodyparts[::-1]

    files = sorted(glob.glob(data_dir+'/lateral_videos/*.avi'))
    files = [f.split('/')[-1] for f in files]

    # data_dir = data_dir.replace('lateral/','')
    dest = data_dir+'/allProfiles/'
    if not os.path.exists(dest):
        os.mkdir(dest)
    if df.shape[0] == len(files):
        for i in range(len(files)):
            df['name'][i] = files[i][9:-4]
    print("Found %d videos to process"%len(files))
    M = len(bodyparts)
    for fName in files:
        meta = videoMetadata(data_dir+'/lateral_videos/'+fName)
        data_file = glob.glob(data_dir+'/labels/'+fName.replace('.avi','*.h5'))[0]
        data = pd.read_hdf(data_file)
        N = data.shape[0]
        xval = np.zeros((N,M))
        yval = np.zeros((N,M))
        for m in range(M):
            xval[:,m] = data[model_lateral][bodyparts[m]]['x'].values
            yval[:,m] = data[model_lateral][bodyparts[m]]['y'].values
        # Smooth values
        xval = smooth(xval,L=10)
        yval = smooth(yval,L=10)

        # Rescale x,y to be [0,1]; y per time point, x across
        yval = (1-(yval-yval.min()) / (yval.max()-yval.min()))
        xval = (xval - xval.min(1).reshape(-1,1)) / (xval.max(1)-xval.min(1)).reshape(-1,1)
        t = np.linspace(0,meta['dur'],len(xval))[::-1]
        dist = pDist(xval)
        dist = dist/dist.max()
        xAng = xval * dist.max(1).reshape(-1,1)/scale + t.reshape(-1,1)
        xAng = xAng - (xAng[:,[-1]] - t.reshape(-1,1))

        ### Measure cycles based on foot angle
        peaks, _ = find_peaks(yval[:,-1])
        meanStep = iqrMean(np.diff(peaks))
        ## Remove outlier peaks
        peaks, _ = find_peaks(yval[:,-1],distance=meanStep)
        swing_idx,yval = getSwingIdx(peaks,yval)
        ### Measure angles
        angles = [measureAngles(yval,xAng,i,i+1,i+2) for i in range(4)]
        cyc_angles = [cycleAngles(peaks,angle) for angle in angles]
        cyc_angles = np.array(cyc_angles)
        ### Check ankle angle for differences
        minAng = cyc_angles.min(2)
        maxAng = cyc_angles.max(2)
        dAng = maxAng-minAng
        dAng[dAng > 120] = 120
        dAng = dAng.mean(1)
        for i in range(len(joints)):
#           df[joints[i]+'_ang'][df.Name in fName] = dAng[i]
            df.at[df.name == fName[9:-4],joints[i]+'_ang'] = dAng[i]
        ### Save cycle_angles
        np.save(dest+fName.replace('.avi','.npy'),cyc_angles)
        makeStickFigure(xval,yval,dist,angles,\
                meta['dur'],fName,cyc_angles,peaks,swing_idx,scale,dest)

    return df
