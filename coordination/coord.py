import pandas as pd
import numpy as np
import glob
import pdb
import warnings
warnings.filterwarnings("ignore")
import os
import matplotlib.pyplot as plt
from gait_analysis.coordination.tools import videoMetadata
#from coordination.tools import videoMetadata
#from speed import estimateSpeed
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.stats import *
#from coordination.constants import *
from scipy.stats import circmean
from matplotlib.gridspec import GridSpec
import matplotlib
from scipy.signal import find_peaks

colors = ['salmon','mediumorchid','deepskyblue']

sod_colors = ['salmon','salmon','black']
days = np.array(['baseline','fasted','recovery'])
groups = np.array(['controls','fasted'])

sod_fill = [True,False,True]
cno_colors = ['black','black','deepskyblue','deepskyblue']
cno_fill = [True,False,True,False]
sodpre_colors = ['mediumorchid','mediumorchid','black']
sodpre_fill = [True,False,True]
sodcno_colors = ['darkorange','darkorange','mediumorchid','mediumorchid']
sodcno_fill = [True,False,True,False]

fillstyles = ['none','full']
params = {'font.size': 14,
          'font.sans-serif': 'Arial',
          'font.weight': 'bold',
          'axes.labelsize':14,
          'axes.titlesize':14,
          'axes.labelweight':'bold',
          'axes.titleweight':'bold',
          'legend.fontsize': 12,
#          'legend.fontweight': 'bold',
         }
matplotlib.rcParams.update(params)


def groupPlot(phi,r,fig,gNames,col):

#    if day == 'baseline':
#        gColors = sod_colors
#        fills = sod_fill
#    elif cScheme == 'cno':
#        gColors = cno_colors
#        fills = cno_fill
#    elif cScheme == 'sodpre':
#        gColors = sodpre_colors
#        fills = sodpre_fill
#    else:
##        gColors = sodcno_colors
#        fills = sodcno_fill
#     pdb.set_trace()
    ax = fig.add_subplot(111,polar=True)
    ax.set_rlim(0,1.1)
    # ax.spines['polar'].set_visible(False)
    # ax.set_axisbelow(True)
    ax.set_theta_offset(np.pi/2)
    # ax.grid(linewidth=3)
    # pdb.set_trace()
    for i in range(len(phi)):
        # lColor = colors[np.where(days==gNames[i].split('_')[0])[0][0]]
        # lFill = fillstyles[np.where(groups==gNames[i].split('_')[1])[0][0]]
        lFill = fillstyles[1]
        ax.plot((10,10),color=col[i],label=gNames[i].replace('_',' '),
                linestyle='none',
               marker='>',fillstyle=lFill,markersize=10)
        ax.annotate("",xytext=(0.0,0.0),xy=(phi[i],r[i]),
                   arrowprops=dict(color=col[i],width=0.2,lw=3,fill=(lFill=='full')))
    # meanPhi = circmean(phi)
    # meanR = np.mean(r)

#    ax.plot((0,0),color='firebrick',label='Mean vector')
#    ax.annotate("",xytext=(0.0,0.0),xy=(meanPhi,meanR*1.05),
#               arrowprops=dict(color='firebrick',lw=4,width=0.75))
    return fig

def meanVector(phi,files,fig,cScheme,gName,idx,scatter=False):
#    pdb.set_trace()
    N = phi.shape[0]
    groupPhi = np.zeros(N)
    groupR = np.zeros(N)
#    ax = fig.add_subplot(gs[pIdx//nR,pIdx%nC],polar=True)
    ax = fig.add_subplot(111,polar=True)

    # ax.set_rlim(0,1.1)
    # ax.spines['polar'].set_visible(False)
    # ax.set_axisbelow(True)
    # ax.set_theta_offset(np.pi/2)
    # ax.grid(linewidth=2)

    # pdb.set_trace()

    # lColor = colors[np.where(days==gName.split('_')[0])[0][0]]
    # lFill = fillstyles[np.where(groups==gName.split('_')[1])[0][0]]

    lFill = 'full'

    for i in range(N):
        animPhi, animR = circular_mean(phi[i])
        groupPhi[i], groupR[i] = animPhi, animR
        # pdb.set_trace()

        ax.plot((0,animPhi),(0,animR),color=cScheme,marker='o',fillstyle=lFill,linestyle='', markeredgecolor='white', markersize=12)
            # pdb.set_trace()
        # else:
        #     ax.annotate("",xytext=(0.0,0.0),xy=(animPhi,animR*1.01),
        #            arrowprops=dict(color='dimgray',width=0.2,lw=2))
    ax.set_title('Angles for '+locKeys[idx]+' limb coordination')
    meanPhi, meanR = circular_mean(groupPhi,r=groupR)

    ax.plot((10,10),color=cScheme,label=gName,
                linestyle='none',
               marker='>',fillstyle=lFill,markersize=10)
    ax.annotate("",xytext=(0.0,0.0),xy=(meanPhi,meanR),
                   arrowprops=dict(color=cScheme,width=0.2,lw=3,fill=True))

    # pdb.set_trace()
    # ax.annotate("",xytext=(0.0,0.0),xy=(meanPhi,meanR*1.01),
    #            arrowprops=dict(color=cScheme,lw=3,
    #                            width=0.75,fill=(lFill=='full')))

    return fig, meanPhi, meanR

# def meanVector(data,files,fig,cScheme,gName,key='h',scatter=False):
#     pKey = 'phi_'+key
#     rKey = 'R_'+key
#     N = len(data[pKey])
#     groupPhi = np.zeros(N)
#     groupR = np.zeros(N)
# #    pdb.set_trace()
#     files = np.array([f.split('/')[-1][:20] for f in files])
#     uniq = np.unique(files)
#     ax = fig.add_subplot(111,polar=True)
#     ax.set_rlim(0,1.1)
#     ax.spines['polar'].set_visible(False)
#     ax.set_axisbelow(True)
#     ax.set_theta_offset(np.pi/2)
#     ax.grid(linewidth=2)
#
#     lColor = colors[np.where(days==gName.split('_')[0])[0][0]]
#     lFill = fillstyles[np.where(groups==gName.split('_')[1])[0][0]]
#
#
#     for i in range(N):
#         phi = data[pKey][i]
#         r = data[rKey][i]
#         groupPhi[i] = circmean(phi)
#         groupR[i] = np.mean(r)
#
#     for i in range(len(uniq)):
#         animPhi = circmean(groupPhi[files==uniq[i]])
#         animR = np.mean(groupR[files==uniq[i]])
#         if scatter:
# #            pdb.set_trace()
#             if lFill == 'full':
#                 ax.plot((0,animPhi),(0,animR),color=lColor,marker='o',
#                         fillstyle=lFill,linestyle='', markeredgecolor='white', markersize=12)
#             else:
#                 ax.plot((0,animPhi),(0,animR),color=lColor,marker='o',
#                         fillstyle=lFill,linestyle='', markersize=12)
#
#         else:
#             ax.annotate("",xytext=(0.0,0.0),xy=(animPhi,animR*1.05),
#                    arrowprops=dict(color='dimgray',width=0.2,lw=2))
# #        ax.plot((0,groupPhi[i]),(0,r),color='lightgrey',alpha=0.1,linewidth=4)
#
#     meanPhi = circmean(groupPhi)
#     meanR = np.mean(groupR)
#
#     ax.annotate("",xytext=(0.0,0.0),xy=(meanPhi,meanR*1.05),
#                arrowprops=dict(color=lColor,lw=3,
#                                width=0.75,fill=(lFill=='full')))
# #    ax.plot((0,meanPhi),(0,meanR),color='firebrick',linewidth=6)
#
#
#     return fig, meanPhi, meanR

def iqrMean(data):
    upper_quartile = np.percentile(data, 75)
    lower_quartile = np.percentile(data, 25)
    IQR = upper_quartile-lower_quartile
    quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
    result = data[np.where((data >= quartileSet[0]) & (data <= quartileSet[1]))]
    
    return result.mean()

def heurCircular(xAxis,stride,peaks):

#    peaks = measureCycles(stride)[1]
    stride = 2*(stride-stride.min())/ (stride.max()-stride.min()) - 1

    N = len(peaks)
    phi = np.zeros(N-1)

    for i in range(N-1):

        lIdx = peaks[i]
        uIdx = peaks[i+1]
        y = stride[lIdx:uIdx]
        x = np.linspace(0,2*np.pi,len(y))
        phi[i] = ((4-np.trapz(y,x)) * np.pi/4)

    meanPhi, r = circular_mean(phi)
    return phi, r, meanPhi



# def heurCircular(xAxis,stride,sMean,idxFlag=False):
#
#     idx = np.where(np.diff(stride > sMean)==True)[0]
#
#     stride = 2*(stride-stride.min())/ (stride.max()-stride.min()) - 1
#
#     if len(idx) % 2 != 0:
#         idx = idx[:-1]
#     newIdx = idx.reshape(-1,2)[:,0]
#     N = len(newIdx)-1
#     phi = np.zeros(N)
#
#     for i in range(1,N+1):
#
#         lIdx = newIdx[i-1]
#         uIdx = newIdx[i]
#         y = stride[lIdx:uIdx]
#         x = np.linspace(0,2*np.pi,len(y))
#         phi[i-1] = ((4-np.trapz(y,x)) * np.pi/4) #% 2*np.pi
#
# #    pdb.set_trace()
#     X = np.cos(phi).mean()
#     Y = np.sin(phi).mean()
#     r = np.sqrt(X**2+Y**2)
# #    meanPhi = circmean(phi)
#     meanPhi = np.arctan2(Y,X)
#     if idxFlag:
#         return phi, r, meanPhi, N, idx
#     else:
#         return phi, r, meanPhi, N

def bodyCoordCircular(lStride, rStride):

    lSMean = iqrMean(lStride)
    rSMean = iqrMean(rStride)

    lIdx = np.where(np.diff(lStride > lSMean) == True)[0][::2]
    rIdx = np.where(np.diff(rStride > rSMean) == True)[0][::2]

    N = np.min([len(lIdx),len(rIdx)]) #// 2 -1

#    lIdx = lIdx[:2*N].reshape(-1,2)
#    rIdx = rIdx[:2*N].reshape(-1,2)

# If rStride is ahead of lStride, swap them for computing phase difference
    if iqrMean(np.diff(lIdx)[:N-1]) < iqrMean(np.diff(rIdx)[:N-1]):
        lStride, rStride = rStride, lStride

    phi = np.zeros(N)
    i = 0
    j = 0
#    pdb.set_trace()
    while i < N-1 and j < len(rIdx)-1:

        rStat = 0
        lY = lStride[lIdx[i]:lIdx[i+1]]
        rY = rStride[lIdx[i]:rIdx[j]]
        lStat = np.argmax(lY)

        while len(rY) < (INTERP-1):
            if j < (len(rIdx)-1):
            # Skip index if rStride does not overlap
            # with lStride
                j += 1
                rY = rStride[lIdx[i]:rIdx[j]]
#                stAng[i-1] = (4-np.trapz(y,x)) * np.pi/4
        if len(rY) > INTERP:
            rStat = np.argmax(rY)
            if lStat < rStat or rStat == 0:
                rStat = np.argmin(rY)
                lStat = np.argmin(lY)+INTERP
        if rStat > 0:
            phi[i] = 2*np.pi*(rStat/lStat)    
        i += 1
        j += 1
    phi = phi[phi != 0 ]
    phi = phi % (2*np.pi)
    meanPhi = circmean(phi)
    cosPhi = np.cos(phi)
    sinPhi = np.sin(phi)
    X = cosPhi.mean()
    Y = sinPhi.mean()
    r = np.sqrt(X**2+Y**2)
    
    return phi, meanPhi, r, len(phi)

def circularPlot(phi,r,title_name,fig, gs,row,col):
    meanPhi = circmean(phi)
    # plt.clf()
    ax = fig.add_subplot(gs[row,col],polar=True)
    plt.title(title_name)
    ax.set_rlim(0,1.1)
    ax.spines['polar'].set_visible(False)
    ax.set_axisbelow(True)
    ax.set_theta_offset(np.pi/2)
    T = (len(phi) if len(phi) > 1 else 1)

    ax.scatter(phi,np.ones(T),marker='o',s=12,c='tab:grey') #,label='Individual steps')
    ax.annotate("",xytext=(0.0,0.0),xy=(meanPhi,r),
               arrowprops=dict(color='tab:red',lw=3,width=0.5,fill='full'))
    ax.plot((0,meanPhi),(0,r),color='tab:red') #label=legends[vNum],color=colors[vNum])
#    plt.legend() 
    return fig

def cadencePlot(movDur, lStride, rStride, fig, gs,row,col,circPlot=True):
    #    plt.box(False)
#    pdb.set_trace()
#     plt.clf()
    lSMean = iqrMean(lStride)
    rSMean = iqrMean(rStride)
    
    sMean = lSMean - rSMean
    stride = lStride-rStride
    T = len(lStride)
    xAxis = np.linspace(0,movDur,T)

#    phi, R, meanPhi, N = heurCircular(xAxis,stride,sMean)
#    if circPlot:
#       fig = circularPlot(phi,R,fig,gs,1)

    ax = fig.add_subplot(gs[row,col])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.plot(xAxis,stride,label='Relative position of hind limbs')
    plt.xlabel('Duration (s)')
    plt.ylabel('Stride length (mm)')
#    idx = np.where(np.diff(stride > sMean) == True)[0]
    _,idx = measureCycles(stride)
    plt.plot(xAxis[idx],stride[idx],'o',label='Possible full cycle',markersize=4) 
    plt.plot(xAxis,np.ones(T)*sMean,'--',color='dimgrey',label='Mean crossing point')
    plt.legend(loc='upper left')
    return fig    
#    return phi, meanPhi, R, fig

def measureCycles(stride):
    peaks,_ = find_peaks(stride)
    thresh = np.diff(peaks).mean()
    peaks,_ = find_peaks(stride,distance=thresh*0.75)
    return len(peaks),peaks

def bodyPosCoord(ipFile,speedMean,avgSpeed,speedSmFactor, meta):

#    model = ipFile.split('cms')[1].split('.')[0]
    data = pd.read_hdf(ipFile)
    speedSmFactor = int(speedSmFactor)
    fL = np.asarray(data[model][mrkr[3]]['x'])
    fL = np.convolve(fL, np.ones((smFactor,))/smFactor, mode='valid')
    fR = np.asarray(data[model][mrkr[5]]['x'])
    fR = np.convolve(fR, np.ones((smFactor,))/smFactor, mode='valid')
    hL = np.asarray(data[model][mrkr[4]]['x'])
    hL = np.convolve(hL, np.ones((smFactor,))/smFactor, mode='valid')
    hR = np.asarray(data[model][mrkr[6]]['x'])
    hR = np.convolve(hR, np.ones((smFactor,))/smFactor, mode='valid')
    
    bodyPos = np.asarray([data[model][speedMarkers[i]]['x'] 
                          for i in range(len(speedMarkers))]).mean(0)
    torsoPos = np.asarray([data[model][speedMarkers[i]]['x'] 
                          for i in range(4,len(speedMarkers))]).mean(0)

#    pdb.set_trace()
    bodyLen = (-np.asarray([data[model][speedMarkers[i]]['x'] 
                          for i in range(1,4)]).mean(0) +
              np.asarray(data[model][speedMarkers[0]]['x'])) * meta['xPixW']/10
    ## Sort bodylength in decreasing order and use first 10% of estimates
    bodyLen = np.sort(bodyLen)[::-1][:int(0.1*meta['nFrame'])]
    bodyLen = iqrMean(bodyLen)
    partition = int(meta['imW']/2)
    intervals = np.arange(3) * partition 
    locHist = plt.hist(torsoPos,bins=intervals)[0]/meta['nFrame']
#    pdb.set_trace()
    bodyPos = bodyPos[smFactor-1:]
    # Compute the distance between right and left paws
    hLStride = (bodyPos-hL) * meta['xPixW']
    hLStride = np.convolve(hLStride, np.ones((speedSmFactor,))/speedSmFactor, mode='valid')
    hRStride = (bodyPos-hR) * meta['xPixW']
    hRStride = np.convolve(hRStride, np.ones((speedSmFactor,))/speedSmFactor, mode='valid')
    fLStride = (fL-bodyPos) * meta['xPixW']
    fLStride = np.convolve(fLStride, np.ones((speedSmFactor,))/speedSmFactor, mode='valid')
    fRStride = (fR-bodyPos) * meta['xPixW']
    fRStride = np.convolve(fRStride, np.ones((speedSmFactor,))/speedSmFactor, mode='valid')

    # Exclude strides when animal is not moving speed = 0
    idx = ((speedMean) > 0)
    hLStride = hLStride[:len(idx)][idx]
    hRStride = hRStride[:len(idx)][idx]
    fLStride = fLStride[:len(idx)][idx]
    fRStride = fRStride[:len(idx)][idx]
    
    # compute avg speed based on non-dragging portions
    avgSpeed = speedMean[idx][::int(meta['fps']/speedSmFactor)].mean()

    hLMean = iqrMean(hLStride)
    hRMean = iqrMean(hRStride)
    fLMean = iqrMean(fLStride)
    fRMean = iqrMean(fRStride)

    # Duration of movement
    movDur = np.sum(idx == True)/len(speedMean) * meta['dur']    

    # Check frames where animal is not moving

    xAxis = np.linspace(0,movDur,len(hLStride))
    xAxisNew = np.linspace(0,movDur,INTERP*len(hLStride))

    # Interpolate for better zero crossing detections
    hLStride = np.interp(xAxisNew, xAxis, hLStride)
    fLStride = np.interp(xAxisNew, xAxis, fLStride)
    hRStride = np.interp(xAxisNew, xAxis, hRStride)
    fRStride = np.interp(xAxisNew, xAxis, fRStride)

    #pdb.set_trace()
    # Count the number of zero crossings for the entire duration
    # Obtain cadence steps/second 
    hLCadence = (measureCycles(hLStride))[0]/movDur
    fLCadence = (measureCycles(fLStride))[0]/movDur
    hRCadence = (measureCycles(hRStride))[0]/movDur
    fRCadence = (measureCycles(fRStride))[0]/movDur


#    hLCadence = (np.sum(np.diff(hLStride > hLMean))/2)/movDur
#    fLCadence = (np.sum(np.diff(fLStride > fLMean))/2)/movDur
#    hRCadence = (np.sum(np.diff(hRStride > hRMean))/2)/movDur
#    fRCadence = (np.sum(np.diff(fRStride > fRMean))/2)/movDur
    
    # Estimate average stride length using cadence and average speed
    hLStep = avgSpeed/hLCadence
    fLStep = avgSpeed/fLCadence
    hRStep = avgSpeed/hRCadence
    fRStep = avgSpeed/fRCadence

    return (hLCadence, hRCadence, fLCadence, fRCadence),\
            (hLStride, hRStride, fLStride, fRStride),\
            (hLStep, hRStep, fLStep, fRStep), movDur, bodyLen, locHist



def coordProfiler(data_path,saveFlag=False,plotFlag=False):
    """
    Input: Pandas frame with tracks for each marker
    Output: Stride, cadence, coordination plots

    Using the tracks from DeepLabCut estimate the coordination of the animal
    """
    os.chdir(data_path)
    files = sorted(glob.glob('*.h5'))
#    pdb.set_trace()
    if not os.path.exists(cdProfLoc):
        os.mkdir(cdProfLoc)
        print('Coordination profiles will be saved in'+cdProfLoc)
    else: 
        print('Using existing location to save coordination profiles at'+cdProfLoc)

    vidFiles = [ f.split('cms')[0]+'cms.avi' for f in files]
    vidFiles = ['../'+f for f in vidFiles]

    for i in range(len(files)):
        ipFile = files[i]
        vid = vidFiles[i]
        print("\nProcessing tracks for "+vid)

        # Load video metadata
        meta = videoMetadata(vid)

        # Measure the speed from tracks
        beltSpeed = ipFile.split('cms')[0].split('_')[-1]
        beltSpeed = float(beltSpeed) * 10
        print('Belt speed is : %.2f cm/s'% (beltSpeed/10))

        _, speedMean, avgSpeed = estimateSpeed(ipFile, beltSpeed, meta, vid,plotSpeed=plotFlag)

        lCadence, rCadence, lStep,\
                rStep, lStride, rStride = estimateCoord(ipFile, vid, meta, speedMean, avgSpeed)

#        lCadence, rCadence, lStep,\
#        hindCoord(ipFile, vid, meta, speedMean, avgSpeed,meta['fps'])
        fig = plt.figure(figsize=(16,10))
        gs = GridSpec(3,3,figure=fig)

        fig = plotCadence(vid,hCadence,fCadence,avgSpeed,xAxisNew,
                    hL,hR,fL,fR,hStep,fStep,fig,gs,relPos=False)

        fig = plotPolar(vid,hStride,fStride,xStride,hStep,fStep,meta['fps'],fig,gs)
        #fig.suptitle('Coordination analysis for '+vid.split('.avi')[0].split('..')[1])
        plt.rcParams.update({'font.size':14})
        fig.tight_layout()
        plt.savefig(cdProfLoc+vid.split('.avi')[0].split('..')[1]+'_coordProfile.pdf')

   

        print('Subject '+vid+' .\nLeft Cadence: %.2f Hz, Right Cadence: %.2f Hz\
              \nUsing Avg. speed %.2f cm/s, Avg. left stride: %.2f cm, Avg. right stride: %.2f cm'\
              %(lCadence,rCadence,avgSpeed,lStep,rStep))
        if saveFlag:
            np.savez(cdProfLoc+vid.split('.avi')[0].split('..')[1]+'_coord.npz',lCadence=lCadence,\
                    rCadence=rCadence,lStep=lStep,rStep=rStep,
                    lStride=lStride,rStride=rStride)

############# Coordination profiler ###################

def plotPolar(vid,hStride,fStride,xStride,hStep,fStep,fps,fig,gs):

    idx = np.where(np.diff(hStride > hStride.mean())==True)[0]
    if len(idx) % 2 != 0: 
        idx = idx[:-1]
    newIdx = idx.reshape(-1,2)[:,0]
    N = len(newIdx)-1
    stAng = np.zeros(N)
    cosPhi = np.zeros(N)
    sinPhi = np.zeros(N)
    for i in range(1,N+1):
        lIdx = newIdx[i-1]
        uIdx = newIdx[i]
        y = hStride[lIdx:uIdx]
        x = np.linspace(0,2*np.pi,len(y))
        stAng[i-1] = (4-np.trapz(y,x)) * np.pi/4
        cosPhi[i-1] = np.cos(stAng[i-1])
        sinPhi[i-1] = np.sin(stAng[i-1])
    X = cosPhi.mean()
    Y = sinPhi.mean()
    r = np.sqrt(X**2+Y**2)
#    meanAng = circmean(stAng)
    meanAng = np.arctan(Y/X)
    plt.figure(figsize=(16,10))
#    ax = fig.add_subplot(gs[1,0],polar=True)
    ax = plt.subplot(121,polar=True)
    ax.set_rlim(0,1.1)
    ax.set_theta_offset(np.pi/2)
    ax.scatter(stAng,np.ones(N),marker='o',label='Individual steps')
    ax.annotate("",xytext=(0.0,0.0),xy=(meanAng,r),
               arrowprops=dict(facecolor='black',width=0.5))
    ax.plot((0,meanAng),(0,r),label='The mean step',color='k')
    plt.legend()
    plt.title("L-R coord. of Hind limbs \
              \nNo. of steps:%d; Avg. step len. %.2f cm\
              \nPhase conc.: %.2f; Mean phase: %.2f°"%(N,hStep,r,meanAng*180/np.pi))
#    plt.savefig(cdProfLoc+vid.split('.avi')[0].split('..')[1]+'_polar.pdf')
    

    ### Plot front limbs
    idx = np.where(np.diff(fStride > fStride.mean())==True)[0]
    if len(idx) % 2 != 0: 
        idx = idx[:-1]
    newIdx = idx.reshape(-1,2)[:,0]
    N = len(newIdx)-1
    stAng = np.zeros(N)
    cosPhi = np.zeros(N)
    sinPhi = np.zeros(N)
    for i in range(1,N+1):
        lIdx = newIdx[i-1]
        uIdx = newIdx[i]
        y = fStride[lIdx:uIdx]
        x = np.linspace(0,2*np.pi,len(y))
        stAng[i-1] = (4-np.trapz(y,x)) * np.pi/4
        cosPhi[i-1] = np.cos(stAng[i-1])
        sinPhi[i-1] = np.sin(stAng[i-1])
    X = cosPhi.mean()
    Y = sinPhi.mean()
    r = np.sqrt(X**2+Y**2)
    meanAng = circmean(stAng)
#    ax = plt.subplot(122,polar=True)
    ax = fig.add_subplot(gs[1,1],polar=True)

    ax.set_rlim(0,1.1)
    ax.set_theta_offset(np.pi/2)
    ax.scatter(stAng,np.ones(N),marker='o',label='Individual steps')
    ax.annotate("",xytext=(0.0,0.0),xy=(meanAng,r),
               arrowprops=dict(facecolor='black',width=0.5))
    ax.plot((0,meanAng),(0,r),label='The mean step',color='k')
    plt.legend()
    plt.title("L-R coordination of Fore limbs \
              '\nNo. of steps:%d; Avg. step len. %.2f cm\
              \nPhase conc.: %.2f; Mean phase: %.2f°"%(N,fStep,r,meanAng*180/np.pi))

#    plt.savefig(cdProfLoc+vid.split('.avi')[0].split('..')[1]+'_polar.pdf')

    ### Plot between fL vs hR limbs
    idx = np.where(np.diff(xStride > xStride.mean())==True)[0]
    if len(idx) % 2 != 0: 
        idx = idx[:-1]
    newIdx = idx.reshape(-1,2)[:,0]
    N = len(newIdx)-1
    stAng = np.zeros(N)
    cosPhi = np.zeros(N)
    sinPhi = np.zeros(N)
    for i in range(1,N+1):
        lIdx = newIdx[i-1]
        uIdx = newIdx[i]
        y = xStride[lIdx:uIdx]
        x = np.linspace(0,2*np.pi,len(y))
        stAng[i-1] = (4-np.trapz(y,x)) * np.pi/4
        cosPhi[i-1] = np.cos(stAng[i-1])
        sinPhi[i-1] = np.sin(stAng[i-1])
    X = cosPhi.mean()
    Y = sinPhi.mean()
    r = np.sqrt(X**2+Y**2)
    meanAng = circmean(stAng)
#    ax = plt.subplot(122,polar=True)
    ax = fig.add_subplot(gs[1,2],polar=True)

    ax.set_rlim(0,1.1)
    ax.set_theta_offset(np.pi/2)
    ax.scatter(stAng,np.ones(N),marker='o',label='Individual steps')
    ax.annotate("",xytext=(0.0,0.0),xy=(meanAng,r),
               arrowprops=dict(facecolor='black',width=0.5))
    ax.plot((0,meanAng),(0,r),label='The mean step',color='k')
    plt.legend()
    plt.title("Coordination bw front left vs hind right limbs \
              \nPhase conc.: %.2f; Mean phase: %.2f°"%(r,meanAng*180/np.pi))

    return fig


def plotCadence(vid,hCadence,fCadence,avgSpeed,xAxis,
                hL,hR,fL,fR,hStep,fStep,fig,gs,relPos=False,plotSave=True):
#    pdb.set_trace()
    ## Normalize between[0,1]
    hL = (hL-hL.mean())/hL.std()
    hR = (hR-hR.mean())/(hR.std())
    fL = (fL-fL.mean())/fL.std()
    fR = (fR-fR.mean())/fR.std()
 
#    plt.figure(figsize=(16,10))
    ax1 = fig.add_subplot(gs[0,:])
    plt.title('Subject '+vid.split('/')[1].split('.')[0]+' .\nHind Cadence: %.2f Hz, Fore Cadence: %.2f Hz\
              \nAvg. speed %.2f cm/s, Avg. hind stride: %.2f cm, Avg. fore stride: %.2f cm'\
              %(hCadence,fCadence,avgSpeed,hStep,fStep))
    if relPos:
        hL = hL - hR
        legend = 'Hind Limb rel.pos'
        plt.ylim([-5,5])
    else:
        legend = 'Hind Left pos.'

    plt.plot(xAxis,np.ones(len(xAxis))*hL.mean(),'--',color='lightgrey')#,label='Mean crossing point')
    
    plt.plot(xAxis,hL,label=legend)
    plt.xlabel('Duration (s)')
#    plt.ylabel('Phase difference between hind limbs')

    idx = np.where(np.diff(hL > hL.mean()) == True)[0]
    plt.plot(xAxis[idx[::2]],hL[idx[::2]],'o')#,label='Possible full cycle') 
#    plt.plot(xAxis[idx[1::2]],hL[idx[1::2]],'o',label='Possible full cycle') 
    #    plt.plot(np.linspace(0,dur,len(speedMean)), speedMean*(np.abs(speedMean) > 5))
    if not relPos:    
        hR -= 2
        plt.plot(xAxis,np.ones(len(xAxis))*hR.mean(),'--',color='lightgrey')#,label='Mean crossing point')
        plt.plot(xAxis,hR,label='Hind Right pos.')
        plt.xlabel('Duration (s)')
    #    plt.ylabel('Phase difference between hind limbs')
        
        idx = np.where(np.diff(hR > hR.mean()) == True)[0]
        plt.plot(xAxis[idx[::2]],hR[idx[::2]],'o',label='Possible full cycle') 
#    plt.plot(xAxis[idx[1::2]],hR[idx[1::2]],'o',label='Possible full cycle') 
#    plt.ylim([-1.2,2])
    #    plt.plot(np.linspace(0,dur,len(speedMean)), speedMean*(np.abs(speedMean) > 5))
        plt.ylim([-6,7])
    plt.legend(loc='upper left')

    plt.grid()

    fStride = fL
    ax2 = fig.add_subplot(gs[2,:])
    if relPos:
        fL = fL - fR
        legend = 'Fore Limb rel.pos'
        plt.ylim([-5,5])

    else:
        legend = 'Fore Left pos.'


#    plt.subplot(2,1,2)
    plt.plot(xAxis,np.ones(len(xAxis))*fL.mean(),'--',color='lightgrey')#,label='Mean crossing point')
    _,idx = measureCycles(fL)
#    idx = np.where(np.diff(fL > fL.mean()) == True)[0]
    plt.plot(xAxis,fL,label=legend)
    plt.plot(xAxis[idx[::2]],fL[idx[::2]],'o')#,label='Possible full cycle') 
#    plt.plot(xAxis[idx[1::2]],fL[idx[1::2]],'o',label='Possible full cycle') 
    plt.xlabel('Duration (s)')
    if not relPos:

        fR -= 2
        plt.plot(xAxis,np.ones(len(xAxis))*fL.mean(),'--',color='lightgrey')#,label='Mean crossing point')
        _,idx = measureCycles(fR)
#        idx = np.where(np.diff(fR > fR.mean()) == True)[0]
        plt.plot(xAxis,fR,label='Fore Right pos.')
        plt.plot(xAxis[idx[::2]],fR[idx[::2]],'o',label='Possible full cycle') 
    #    plt.plot(xAxis[idx[1::2]],fR[idx[1::2]],'o',label='Possible full cycle') 

        plt.ylim([-6.,7])
    plt.xlabel('Duration (s)')
#
    plt.grid()
#    plt.ylabel('Phase difference between front limbs')
    #    plt.plot(np.linspace(0,dur,len(speedMean)), speedMean*(np.abs(speedMean) > 5))
    plt.legend(loc='upper left')
#    if plotSave:
#        plt.savefig(cdProfLoc+vid.split('.avi')[0].split('..')[1]+'_coordProfile.pdf')
    return fig



def hindCoord(ipFile,vid,meta,speedMean,avgSpeed,fps):

    model = ipFile.split('cms')[1].split('.')[0]
    data = pd.read_hdf(ipFile)
    
    hL = np.asarray(data[model][mrkr[4]]['x'])* meta['xPixW']
    hL = np.convolve(hL, np.ones((smFactor,))/smFactor, mode='valid')
    hR = np.asarray(data[model][mrkr[6]]['x']) * meta['xPixW']
    hR = np.convolve(hR, np.ones((smFactor,))/smFactor, mode='valid')
    
    # Compute the distance between right and left paws
    hL = 2*(hL-hL.min())/(hL.max()-hL.min()) - 1
    hR = 2*(hR-hR.min())/(hR.max()-hR.min()) - 1

    # Check frames where animal is not moving
    idx = (np.abs(speedMean) > speedThr)

    # Set stride length to be zero when animal is not moving
    hL[:-speedSmFactor][~idx] = 0
    hR[:-speedSmFactor][~idx] = 0

#    pdb.set_trace()

    ### Plot circular plot for hind limbs
    idx = np.where(np.diff(hL > hL.mean())==True)[0]
    if len(idx) % 2 != 0: 
        idx = idx[:-1]
    newIdx = idx.reshape(-1,2)[:,0]
    N = len(newIdx)-1
    stAng = np.zeros(N)
    yLtime = np.zeros(N)
    yRtime = np.zeros(N)
    if np.diff(hL)[0] > 0:
        getTime = np.argmax
    else:
        getTime = np.argmin

    for i in range(1,N+1):
        plt.clf()
        lIdx = newIdx[i-1]
        uIdx = newIdx[i]
        yL = hL[lIdx:uIdx]
        yLtime[i-1] = (getTime(yL)+1)/fps

        yR = hR[lIdx:uIdx]
        yRtime[i-1] = (getTime(yR)+1)/fps

        plt.plot(yL)
        plt.plot(yR)


    stAng = yLtime/yRtime * 2*np.pi
    X = np.cos(stAng).mean()
    Y = np.sin(stAng).mean()
    r = np.sqrt(X**2+Y**2)
    meanAng = np.arctan(Y/X) #circmean(stAng)
#
#    pdb.set_trace()
    plt.polar(stAng,np.ones(N),'o')
    plt.polar((0,meanAng),(0,r))
    plt.savefig(cdProfLoc+vid.split('.avi')[0].split('..')[1]+'_polarProfile.pdf')

    return
#    return hCadence, fCadence, hStep, fStep, hStride, fStride 


def estimateCoord(ipFile,vid,meta,speedMean,avgSpeed):

    model = ipFile.split('cms')[1].split('.')[0]
    data = pd.read_hdf(ipFile)
    
    fL = np.asarray(data[model][mrkr[3]]['x'])
    fL = np.convolve(fL, np.ones((smFactor,))/smFactor, mode='valid')
    fR = np.asarray(data[model][mrkr[5]]['x'])
    fR = np.convolve(fR, np.ones((smFactor,))/smFactor, mode='valid')
    hL = np.asarray(data[model][mrkr[4]]['x'])
    hL = np.convolve(hL, np.ones((smFactor,))/smFactor, mode='valid')
    hR = np.asarray(data[model][mrkr[6]]['x'])
    hR = np.convolve(hR, np.ones((smFactor,))/smFactor, mode='valid')
    
    bodyPos = np.asarray([data[model][speedMarkers[i]]['x'] 
                          for i in range(len(speedMarkers))]).mean(0)

    # Compute the distance between right and left paws
    hStride = (hL-hR) * meta['xPixW']
    # Rescale the distance to be between [-1,1]
    hStride = 2*(hStride-hStride.min())/(hStride.max()-hStride.min()) - 1
    fStride = (fL-fR) * meta['xPixW']
    fStride = 2*(fStride-fStride.min())/(fStride.max()-fStride.min()) - 1
    xStride = -(fL-hR)
    xStride = 2*(xStride-xStride.min())/(xStride.max()-xStride.min()) - 1


#    pdb.set_trace()
    # Check frames where animal is not moving
    idx = (np.abs(speedMean) > speedThr)

    # Set stride length to be zero when animal is not moving
    hStride[:-speedSmFactor][~idx] = 0
    fStride[:-speedSmFactor][~idx] = 0
    xStride[:-speedSmFactor][~idx] = 0

    xAxis = np.linspace(0,meta['dur'],len(hStride))
    xAxisNew = np.linspace(0,meta['dur'],4*len(fStride))

    # Interpolate for better zero crossing detections
    hStride = np.interp(xAxisNew, xAxis, hStride)
    fStride = np.interp(xAxisNew, xAxis, fStride)
    xStride = np.interp(xAxisNew, xAxis, xStride)

    hL = np.interp(xAxisNew, xAxis, hL)
    hR = np.interp(xAxisNew, xAxis, hR)
    fL = np.interp(xAxisNew, xAxis, fL)
    fR = np.interp(xAxisNew, xAxis, fR)

    # Count the number of zero crossings for the entire duration
    # Obtain cadence steps/second 
    hCadence = (np.sum(np.diff(hStride > hStride.mean()))/2)/meta['dur']
    fCadence = (np.sum(np.diff(fStride > fStride.mean()))/2)/meta['dur']
    
    # Estimate average stride length using cadence and average speed
    hStep = avgSpeed/hCadence
    fStep = avgSpeed/fCadence

    fig = plt.figure(figsize=(18,20))
    gs = GridSpec(3,3,figure=fig)

    fig = plotCadence(vid,hCadence,fCadence,avgSpeed,xAxisNew,
                hL,hR,fL,fR,hStep,fStep,fig,gs,relPos=False)

    fig = plotPolar(vid,hStride,fStride,xStride,hStep,fStep,meta['fps'],fig,gs)
    #fig.suptitle('Coordination analysis for '+vid.split('.avi')[0].split('..')[1])
    plt.rcParams.update({'font.size':14})
    fig.tight_layout()
    plt.savefig(cdProfLoc+vid.split('.avi')[0].split('..')[1]+'_coordProfile.pdf')

    return hCadence, fCadence, hStep, fStep, hStride, fStride 


