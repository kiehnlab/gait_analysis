import pandas as pd
import numpy as np
import glob
import pdb
import warnings
warnings.filterwarnings("ignore")
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from gait_analysis.coordination.tools import videoMetadata
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.accel import *
from gait_analysis.coordination.coord import *

#from coordination.tools import videoMetadata
#from coordination.constants import *
#from coordination.accel import *
#from coordination.coord import *

############## Speed analysis ##########

# def plotSpeedProfile(vid, meta, beltSpeed, avgSpeed,
#                      speedMean, speedStd,saveFlag=True):
#     plt.clf()
#     fig = plt.figure(figsize=(16,10))
#     newFrame = speedMean.size
#     xAxis = np.linspace(0,meta['dur'],newFrame)
#     plt.fill_between( xAxis, speedMean-speedStd, speedMean + speedStd,
#                                       color='gray', alpha=0.3)
#     plt.plot(xAxis,speedMean,label='Avg. Instataneous speed')
#     plt.plot(xAxis,beltSpeed/10*np.ones(newFrame),'--',label='Belt Speed')
#     plt.plot(xAxis,avgSpeed.mean()*np.ones(newFrame),':',label='Avg. Speed')
#     plt.xlabel('Time in s')
#     plt.ylabel('Speed in cm/s')
#     plt.title('Smoothed speed estimates for '+vid.split('/')[1].split('.')[0]+
#               '\n Belt Speed: %.2f \n Avg. Speed: %.2f'%(beltSpeed/10,avgSpeed))
#     plt.legend()
#     if saveFlag:
#         plt.savefig(spProfLoc+vid.split('.avi')[0].split('..')[1]+'_speedProfile.pdf')
#     #return fig
    
def estimateSpeed(ipFile,beltSpeed,meta,vid,speedSmFactor,plotSpeed=True):

#    model = ipFile.split('cms')[1].split('.')[0]
    data = pd.read_hdf(ipFile)
    model = data.keys()[0][0]
    time = 1/meta['fps'] # interval between successive frames in s
    speedAll = []
    speedSmFactor = int(speedSmFactor)

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


    speedStd = speedAll.std(0)
    speedStd = np.convolve(speedStd, np.ones((speedSmFactor,)) / speedSmFactor, mode='valid')

    if plotSpeed:
        speedStd = speedAll.std(0)
        speedStd = np.convolve(speedStd, np.ones((speedSmFactor,))/speedSmFactor, mode='valid')
        plotSpeedProfile(vid, meta, beltSpeed, avgSpeed, speedMean, speedStd)

    return speedAll, speedMean, avgSpeed, speedStd
    

def limbCoord(str_0,str_1,movDur,peaks):

#        lStride, rStride = stride[0], stride[1]
#         str_0_mean = iqrMean(str_0)
#         str_1_mean = iqrMean(str_1)

        # sMean = iqrMean(str_0) - iqrMean(str_1)
        relStride = str_0 - str_1
        T = len(relStride)
        xAxis = np.linspace(0,movDur,T)
        # phi, R, meanPhi, nSteps = heurCircular(xAxis,relStride,sMean)
        phi, R, meanPhi = heurCircular(xAxis,relStride,peaks)

        return phi, R, meanPhi

def plotSpeedProfile(vid, meta, beltSpeed, avgSpeed,
                     speedMean, speedStd, fig, gs,row):
#    plt.clf()
#    plt.figure(figsize=(16,10))
    ax = fig.add_subplot(gs[row,:])
    newFrame = speedMean.size
    xAxis = np.linspace(0,meta['dur'],newFrame)
    plt.fill_between( xAxis, speedMean-speedStd, speedMean + speedStd,
                                      color='gray', alpha=0.3)
    plt.plot(xAxis,speedMean,label='Avg. Instataneous speed')
    plt.plot(xAxis,beltSpeed/10*np.ones(newFrame),'--',label='Belt Speed')
    plt.plot(xAxis,avgSpeed.mean()*np.ones(newFrame),':',label='Avg. Speed')
    plt.xlabel('Time in s')
    plt.ylabel('Speed in cm/s')
    plt.xlim(0,meta['dur'])
    plt.title('Analysis for '+vid.split('/')[-1]+
              '\n Belt Speed: %.2f cm/s \n Avg. Speed: %.2f cm/s'%(beltSpeed/10,avgSpeed))
    plt.legend()
#    if saveFlag:
#   plt.savefig(spProfLoc+vid.split('.avi')[0]+'_speedProfile.pdf')
    return fig


def locomotionProfiler(data_path,tThr,speedSmFactor,grid_number,combination,belt,df,saveFlag=False,plotFlag=False,log=False,plot_speed=False,plot_acc=False):
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
        if belt < 0:
            beltSpeed = ipFile.split('cms')[0].split('_')[-1]
            beltSpeed = float(beltSpeed) * 10
        else:
            beltSpeed = float(belt) * 10
        print('Belt speed is : %.2f cm/s'% (beltSpeed/10))

        speedAll,speedMean,avgSpeed,speedStd = estimateSpeed(ipFile,
                beltSpeed, meta, vid,speedSmFactor,plotSpeed=plotFlag)

        accMean, drgIdx, recIdx, xAxis = estimateAccel(speedMean,meta)

        dragCount, recCount, drgDur, recDur, drgIdx, recIdx = \
                analyseDragRec(drgIdx,recIdx,meta['fps'], tThr)

        cadence, stride, stepLen, movDur, \
                bodyLen,locHist = bodyPosCoord(ipFile, speedMean, avgSpeed,speedSmFactor, meta)

        # ### Coordination of l-r hind limbs
        # phi_heur, R_heur, meanPhi_heur, nSteps = limbCoord(stride[0],stride[1],movDur)
        #
        # ### Coordination of l-r fore limbs
        # phi_fore, R_fore, meanPhi_fore, nSteps_fore = limbCoord(stride[2],stride[3],movDur)
        #
        # ### Coordination of f-h right limbs
        # phi_xR, R_xR, meanPhi_xR, nSteps_xR = limbCoord(stride[1],stride[3],movDur)
        #
        # ### Coordination of f-h left limbs
        # phi_xL, R_xL, meanPhi_xL,nSteps_xL = limbCoord(stride[0],stride[2],movDur)
        #
        # ### Coordination of fL-hR left limbs
        # phi_fLhR, R_fLhR, meanPhi_fLhR,nSteps_fLhR = limbCoord(stride[2],stride[1],movDur)
        #
        # ### Coordination of fR-hL left limbs
        # phi_fRhL, R_fRhL, meanPhi_fRhL,nSteps_fRhL = limbCoord(stride[3],stride[0],movDur)

        # Get step cycles from hind limbs
        nSteps, peaks = measureCycles(stride[0]-stride[1])

        ### Coordination of l-r hind limbs
        phi_heur, R_heur, meanPhi_heur = limbCoord(stride[0],stride[1],movDur,peaks)

        ### Coordination of l-r fore limbs
        phi_fore, R_fore, meanPhi_fore = limbCoord(stride[2],stride[3],movDur,peaks)

        ### Coordination of f-h right limbs
        phi_xR, R_xR, meanPhi_xR = limbCoord(stride[1],stride[3],movDur,peaks)

        ### Coordination of f-h left limbs
        phi_xL, R_xL, meanPhi_xL = limbCoord(stride[0],stride[2],movDur,peaks)

        ### Coordination of fL-hR left limbs
        phi_fLhR, R_fLhR, meanPhi_fLhR = limbCoord(stride[2],stride[1],movDur,peaks)

        ### Coordination of fR-hL left limbs
        phi_fRhL, R_fRhL, meanPhi_fRhL = limbCoord(stride[3],stride[0],movDur,peaks)

        aAxis = np.linspace(0, movDur, accMean.shape[0])
        # pdb.set_trace()
        plt.clf()
        fig = plt.figure(figsize=(30,50))
        gs = GridSpec(grid_number+2,2,figure=fig)
        leg = ['LH','RH','LF','RF']
        col = True
        for i in range(4):
            ax = fig.add_subplot(gs[i//2,col]) 
            col = ~col
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            peaks = measureCycles(stride[i])[1]
            xAxis = np.linspace(0,movDur,len(stride[i]))
            plt.plot(xAxis,stride[i])
            plt.plot(xAxis[peaks],stride[i][peaks],'o')
            plt.title(leg[i]+', N=%d'%(len(peaks)))
        k = 2
        if plot_speed:
            fig = plotSpeedProfile(vid, meta, beltSpeed, avgSpeed, speedMean, speedStd, fig, gs,k)
            k += 1
        if plot_acc:
            fig = plotDragReco(tThr=tThr, xAxis=aAxis, accMean=accMean, drgIdx=drgIdx, recIdx=recIdx, dragCount=dragCount, recCount=recCount, drgDur=drgDur, recDur=recDur, vid=vid,fig=fig,gs=gs,row=k)
            k += 1
        if len(combination) > 0 :
            for j in combination:
                if j == 'Hindlimb("LH_RH")':
                    fig = circularPlot(phi_heur,R_heur, 'LHRH', fig, gs, row=k, col=0)
                    fig = cadencePlot(movDur, stride[0],stride[1], fig, gs,k,1, circPlot=False)
                    k += 1

                elif j == 'Forelimb("LF_RF")':
                    fig = circularPlot(phi_fore,R_fore, 'LFRF', fig, gs, row=k, col=0)
                    fig = cadencePlot(movDur, stride[2],stride[3], fig, gs,k,1, circPlot=False)
                    k += 1

                elif j == 'Homolateral right("RH_RF")':
                    fig = circularPlot(phi_xR,R_xR, 'RHRF', fig, gs, row=k, col=0)
                    fig = cadencePlot(movDur, stride[1],stride[3], fig, gs,k,1, circPlot=False)
                    k += 1

                elif j == 'Homolateral left("LF_LH")':
                    fig = circularPlot(phi_xL,R_xL, 'LFLH', fig, gs, row=k, col=0)
                    fig = cadencePlot(movDur, stride[0],stride[2], fig, gs,k,1, circPlot=False)
                    k += 1

                elif j == 'Contra-lateral frontleft-hindright("LF_RH")':
                    fig = circularPlot(phi_fLhR,R_fLhR, 'LFRH', fig, gs, row=k, col=0)
                    fig = cadencePlot(movDur, stride[2],stride[1], fig, gs,k,1, circPlot=False)
                    k += 1

                elif j == 'Contra-lateral frontright-hindleft("LH_RF")':
                    fig = circularPlot(phi_fRhL,R_fRhL, 'LHRF', fig, gs, row=k, col=0)
                    fig = cadencePlot(movDur, stride[3],stride[0], fig, gs,k,1, circPlot=False)
                    k += 1

        # plt.show()
        plt.tight_layout()
        plt.savefig('../allProfiles/'+(vid.split('/')[-1]).split('.')[0]+'_BOTTOM_VIEW.pdf')

        # fig = plt.figure(figsize=(30,30))
        # gs = GridSpec(2,2,figure=fig)
        # ax = fig.add_subplot(gs[0,:])
        # plt.title('Subject '+vid.split('/')[1]+' .\n Left Cadence: %.2f Hz, Right Cadence: %.2f Hz, nSteps: %d\
        #           \n Using Avg. speed %.2f cm/s, Avg. left stride: %.2f cm, Avg. right stride: %.2f cm'
        #    %((cadence[0]),(cadence[1]),nSteps,avgSpeed,
        #      (stepLen[0]),(stepLen[1])))

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
        df['name'][i] = vid.split('/')[-1].split('.')[0]
        df['bodyLen'][i] = bodyLen
        df['duration'][i], df['mov_dur'][i] = meta['dur'], movDur
        df['belt speed'][i] = beltSpeed / 10
        df['avg.speed'][i] = avgSpeed
        df['peak_acc'][i] = accMean.max()
        df['loc_front'][i], df['loc_rear'][i] = locHist[0], locHist[1]
        df['num_rec'][i], df['num_drag'][i] = recCount + 1, dragCount + 1
        df['count_ratio'][i] = (1 + dragCount) / (1 + recCount)
        df['dur_rec'][i], df['dur_drag'][i] = recDur, drgDur
        # df['num_steps'][i] = nSteps
        df['LH_st_len'][i], df['LF_st_len'][i], df['RH_st_len'][i], df['RF_st_len'][i] = \
            stepLen[0], stepLen[2], stepLen[1], stepLen[3]
        df['LH_st_frq'][i], df['LF_st_frq'][i], df['RH_st_frq'][i], df['RF_st_frq'][i] = \
            cadence[0], cadence[2], cadence[1], cadence[3]
        df['LHRH_ang'][i], df['LHLF_ang'][i], df['RHRF_ang'][i], df['LFRH_ang'][i], df['RFLH_ang'][i], df['LFRF_ang'][
            i] = \
            meanPhi_heur, meanPhi_xL, meanPhi_xR, meanPhi_fLhR, meanPhi_fRhL, meanPhi_fore
        df['LHRH_rad'][i], df['LHLF_rad'][i], df['RHRF_rad'][i], df['LFRH_rad'][i], df['RFLH_rad'][i], df['LFRF_rad'][
            i] = \
            R_heur, R_xL, R_xR, R_fLhR, R_fRhL, R_fore
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
            # data['nSteps']=nSteps
            data['phi_h']=phi_heur
            data['R_h'] = R_heur
            data['phi_f']=phi_fore
            data['R_f']=R_fore
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
    return df



