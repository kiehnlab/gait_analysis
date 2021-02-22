import pandas as pd
import numpy as np
import glob
import pdb
import warnings
warnings.filterwarnings("ignore")
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from coordination.tools import videoMetadata
from coordination.constants import *
from coordination.accel import *
from coordination.coord import *

############## Speed analysis ##########

def plotSpeedProfile(vid, meta, beltSpeed, avgSpeed,
                     speedMean, speedStd,saveFlag=True):
    plt.clf()
    plt.figure(figsize=(16,10))
    newFrame = speedMean.size
    xAxis = np.linspace(0,meta['dur'],newFrame)
    plt.fill_between( xAxis, speedMean-speedStd, speedMean + speedStd,
                                      color='gray', alpha=0.3)
    plt.plot(xAxis,speedMean,label='Avg. Instataneous speed')
    plt.plot(xAxis,beltSpeed/10*np.ones(newFrame),'--',label='Belt Speed')
    plt.plot(xAxis,avgSpeed.mean()*np.ones(newFrame),':',label='Avg. Speed')
    plt.xlabel('Time in s')
    plt.ylabel('Speed in cm/s')
    plt.title('Smoothed speed estimates for '+vid.split('/')[1].split('.')[0]+
              '\n Belt Speed: %.2f \n Avg. Speed: %.2f'%(beltSpeed/10,avgSpeed))
    plt.legend()
    if saveFlag:
        plt.savefig(spProfLoc+vid.split('.avi')[0].split('..')[1]+'_speedProfile.pdf')
    return
    
def estimateSpeed(ipFile,beltSpeed,meta,vid,plotSpeed=True):

#    model = ipFile.split('cms')[1].split('.')[0]
    data = pd.read_hdf(ipFile)
    time = 1/meta['fps'] # interval between successive frames in s
    speedAll = []

    for i in range(len(speedMarkers)):

        m0 = data[model][speedMarkers[i]]
        m0X = np.array(m0['x']) * meta['xPixW']
        m0XSmoothed = np.convolve(m0X, np.ones((smFactor,))/smFactor, mode='valid')
        speed = (-np.diff(m0XSmoothed)/time + beltSpeed)
        
        #Remove outliers
        speed[np.abs(speed) > 3*beltSpeed] = beltSpeed
        speed /= 10 # Convert to cm/s
        speedAll.append(speed)

    speedAll = np.stack(speedAll)

    speedMean = speedAll.mean(0)
    speedMean = np.convolve(speedMean, np.ones((speedSmFactor,))/speedSmFactor, mode='valid')
    avgSpeed = speedMean[::int(meta['fps']/speedSmFactor)].mean()
    print("Avg. Speed: %.2f cm/s"%(avgSpeed))

    if plotSpeed:
        speedStd = speedAll.std(0)
        speedStd = np.convolve(speedStd, np.ones((speedSmFactor,))/speedSmFactor, mode='valid')
        plotSpeedProfile(vid, meta, beltSpeed, avgSpeed, speedMean, speedStd)

    return speedAll, speedMean, avgSpeed
    

def limbCoord(str_0,str_1,movDur):

#        lStride, rStride = stride[0], stride[1]
        str_0_mean = iqrMean(str_0)
        str_1_mean = iqrMean(str_1)

        sMean = iqrMean(str_0) - iqrMean(str_1)
        relStride = str_0 - str_1
        T = len(relStride)
        xAxis = np.linspace(0,movDur,T)
        phi, R, meanPhi, nSteps = heurCircular(xAxis,relStride,sMean)

        return phi, R, meanPhi, nSteps



def locomotionProfiler(data_path,saveFlag=False,plotFlag=False,log=False):
    """
    Input: Pandas frame with tracks for each marker
    Output: Smoothed speed, acceleration and coordination profiles
    """
    os.chdir(data_path)
    vidFiles = sorted(glob.glob('../*.avi'))
    vidFiles.extend(sorted(glob.glob('../*.mp4')))
    if not os.path.exists(spProfLoc):
        os.mkdir(spProfLoc)
        print('Speed profiles will be saved in '+spProfLoc)
    else: 
        print('Using existing location to save speed profiles at '+spProfLoc)
    with open('../speedProfile.csv','w') as f:
        print('Name\tbodyLen\tDuration\tlocFrnt\tlocMid\tlocRear\tBelt Speed\tAvg.Speed\tPeakAcc.\t'\
              'Num_drag\tNum_rec\tCount_Ratio\tDur_drag\tDur_rec\t'\
              'Dur_ratio\tMovDur\tNum_steps\tPhi_heur\tR_heur\t'\
              'hLCad.\thRCad.\t'\
              'fLCad.\tfRCad\thLStride\thRStride\tfLStride\tfRStride',file=f)

    for i in range(len(vidFiles)):

        vid = vidFiles[i]
        if vid.split('.')[-1] == 'avi':
            ipFile = glob.glob(vid.split('/')[1].split('.avi')[0]+'*.h5')[0]
            fName = spProfLoc+vid.split('.avi')[0].split('..')[1]
            print("\n Processing tracks for "+vid)
        else:
            ipFile = glob.glob(vid.split('/')[1].split('.mp4')[0] + '*.h5')[0]
            fName = spProfLoc + vid.split('.mp4')[0].split('..')[1]
            print("\n Processing tracks for " + vid)

        # Load video metadata
        meta = videoMetadata(vid)

        # Measure the speed from tracks
        beltSpeed = ipFile.split('cms')[0].split('_')[-1]
        beltSpeed = float(beltSpeed) * 10
        print('Belt speed is : %.2f cm/s'% (beltSpeed/10))

        speedAll,speedMean,avgSpeed = estimateSpeed(ipFile,
                beltSpeed, meta, vid,plotSpeed=plotFlag)

        accMean, drgIdx, recIdx, xAxis = estimateAccel(speedMean,meta)

        dragCount, recCount, drgDur, recDur, drgIdx, recIdx = \
                analyseDragRec(drgIdx,recIdx,meta['fps'], tThr)

        cadence, stride, stepLen, movDur, \
                bodyLen,locHist = bodyPosCoord(ipFile, speedMean, avgSpeed, meta)

        ### Coordination of l-r hind limbs
        phi_heur, R_heur, meanPhi_heur, nSteps = limbCoord(stride[0],stride[1],movDur)

        ### Coordination of f-h right limbs
        phi_xR, R_xR, meanPhi_xR, nSteps_xR = limbCoord(stride[1],stride[3],movDur)

        ### Coordination of f-h left limbs
        phi_xL, R_xL, meanPhi_xL,nSteps_xL = limbCoord(stride[0],stride[2],movDur)

        ### Coordination of fL-hR left limbs
        phi_fLhR, R_fLhR, meanPhi_fLhR,nSteps_fLhR = limbCoord(stride[2],stride[1],movDur)

        ### Coordination of fR-hL left limbs
        phi_fRhL, R_fRhL, meanPhi_fRhL,nSteps_fRhL = limbCoord(stride[3],stride[0],movDur)


        fig = plt.figure(figsize=(16,10))
        gs = GridSpec(2,2,figure=fig)
        ax = fig.add_subplot(gs[0,:])
        plt.title('Subject '+vid.split('/')[1]+' .\n Left Cadence: %.2f Hz, Right Cadence: %.2f Hz, nSteps: %d\
                  \n Using Avg. speed %.2f cm/s, Avg. left stride: %.2f cm, Avg. right stride: %.2f cm'
           %((cadence[0]),(cadence[1]),nSteps,avgSpeed,
             (stepLen[0]),(stepLen[1])))

        if log:
            with open('../speedProfile.csv','a') as f:
                print(vid.split('/')[1].split('.')[0]+'\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t'\
                        '%.3f\t%.4f\t%d\t%d\t%.4f\t%.4f\t%.4f\t%.4f\t'\
                      '%.4f\t%d\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f'\
                      '\t%.4f\t%.4f\t%.4f\t%.4f'
                        %(bodyLen,meta['dur'],locHist[0],0,locHist[1],beltSpeed/10,avgSpeed,accMean.max(),\
                            1+dragCount,1+recCount,(1+dragCount)/(1+recCount),\
                            drgDur,recDur,(tThr+drgDur)/(tThr+recDur),\
                          movDur,nSteps,180/np.pi*meanPhi_heur,\
                          R_heur,(cadence[0]),\
                          cadence[1],cadence[2],cadence[3],stepLen[0],\
                         stepLen[1],stepLen[2],stepLen[3]),file=f)
        if saveFlag:
            data = dict.fromkeys(keys,None)
            data['speed'] = speedAll
            data['lCad'] = cadence[0]
            data['rCad'] = cadence[1]
            data['flCad'] = cadence[2]
            data['frCad'] = cadence[3]
            data['avg'] = avgSpeed
            data['rStLen'] = stepLen[1]
            data['lStLen'] = stepLen[0]
            data['frStLen'] = stepLen[3]
            data['flStLen'] = stepLen[2]
            data['nSteps']=nSteps
            data['phi_h']=phi_heur
            data['R_h'] = R_heur
            data['phi_xR']=phi_xR
            data['R_xR'] = R_xR
            data['phi_xL']=phi_xL
            data['R_xL'] = R_xL
            data['phi_fLhR']=phi_fLhR
            data['R_fLhR'] = R_fLhR
            data['phi_fRhL']=phi_fRhL
            data['R_fRhL'] = R_fRhL
            data['movDur']=movDur
            data['rStride']=stride[1]
            data['lStride']=stride[0]
            data['fRStride']=stride[3]
            data['fLStride']=stride[2]
            np.save(fName+'_Profile.npy',data)




