import pandas as pd
import numpy as np
import glob
import pdb
import warnings
warnings.filterwarnings("ignore")
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.stats import circmean
from gait_analysis.coordination.tools import videoMetadata
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.accel import *
from gait_analysis.coordination.coord import bodyPosCoord, bodyCoordCircular, circularPlot, cadencePlot

#from coordination.tools import videoMetadata
#from coordination.constants import *
#from coordination.accel import *
#from coordination.coord import bodyPosCoord, bodyCoordCircular, circularPlot, cadencePlot

############## Speed analysis ##########
    
def processDict(dFiles):
    allData = allData=dict.fromkeys(keys,[])

    for dFname in dFiles:
        data = np.load(dFname,allow_pickle=True).item()
        for key,value in data.items():
            allData[key] = allData[key]+[value]

#    for k in keys:
#        allData[k] = np.hstack(allData[k])
    return allData

def combinedPlot(data_path,combination_list,saveFlag=False,paperPlot=True):
#     """
#     Input: Npz file with all processed data
#     Output: Combined plots for triplicates
#
#     Using the tracks from DeepLabCut estimate the speed of the animal
#     and estimate the instantaneous acceleration.
#     """
# #    pdb.set_trace()
#     os.chdir(data_path)
#     files = sorted(glob.glob('../allProfiles/*_Profile.npy'))
#     uniqF = [f.split('_0deg')[0] for f in files];
#     uniqF = list(np.unique(uniqF))
#
#     for f in (uniqF):
#
#         dataFiles = sorted(glob.glob(f+'*_Profile.npy'))
#         allData = processDict(dataFiles)
#         fig = plt.figure(figsize=(16,10))
#         gs = GridSpec(2,2,figure=fig,hspace=0.3)
#         nVid = len(dataFiles)
#
#         for j in range(nVid):
#
#             if not paperPlot:
#                 fig = circularPlot(allData['phi'][j], allData['R'][j], fig, gs,
#                                gsNum=0,vNum=j)
#             fig = circularPlot(allData['phi_h'][j], allData['R_h'][j], fig,
#                                gs,gsNum=1,vNum=j,paperPlot=paperPlot)
#
#         ax = fig.add_subplot(gs[0,:])
#         plt.title('Subject '+f+' .\n Left Cadence: %.2f Hz, Right Cadence: %.2f Hz, nSteps: %d\
#                \n Using Avg. speed %.2f cm/s, Avg. left stride: %.2f cm, Avg. right stride: %.2f cm'
#                   %(np.mean(allData['lCad']),np.mean(allData['rCad']),
#                     sum(allData['nSteps']),np.mean(allData['avg']),
#                     np.mean(allData['lStLen']),np.mean(allData['rStLen'])))
#         for k in keys:
#             allData[k] = np.hstack(allData[k])
#
#         if not paperPlot:
#             fig = circularPlot([circmean(allData['phi'])],
#                            np.mean(allData['R']), fig, gs,gsNum=0,vNum=-1)
#
#         fig = circularPlot([circmean(allData['phi_h'])],np.mean(allData['R_h']),
#                            fig, gs, gsNum=1, vNum=-1,paperPlot=paperPlot)
#
# #        pdb.set_trace()
#         fig = cadencePlot(sum(allData['movDur']), allData['lStride'],
#                              allData['rStride'], fig, gs,circPlot=False)
# #        plt.legend()
#         plt.savefig(f+'.pdf')
    """
    Input: Npz file with all processed data
    Output: Combined plots for triplicates

    Using the tracks from DeepLabCut estimate the speed of the animal
    and estimate the instantaneous acceleration.
    """
#    pdb.set_trace()
    list = []
    os.chdir(data_path)
    files = sorted(glob.glob('../allProfiles/*_Profile.npy'))
    uniqF = [f.split('_0deg')[0] for f in files];
    uniqF = list(np.unique(uniqF))
    for f in (uniqF):
        for k in combination_list:
            dataFiles = sorted(glob.glob(f + '*_Profile.npy'))

            allData = processDict(dataFiles)
            fig = plt.figure(figsize=(16, 10))
            gs = GridSpec(1,3 , figure=fig, hspace=0.3)
            nVid = len(dataFiles)
            for j in range(nVid):
                if k == 'Hindlimb("LH_RH")':
                    x_circ_data = allData['phi_h'][j]
                    y_circ_data = allData['R_h'][j]
                    x_circ1_data = [circmean(allData['phi_h'][j])]
                    y_circ1_data = np.mean(allData['R_h'][j])

                elif k == 'Forelimb("LF_RF")':
                    x_circ_data = allData['phi_f'][j]
                    y_circ_data = allData['R_f'][j]
                    x_circ1_data = [circmean(allData['phi_f'][j])]
                    y_circ1_data = np.mean(allData['R_f'][j])

                elif k == 'Homolateral right("RH_RF")':
                    x_circ_data = allData['phi_xR'][j]
                    y_circ_data = allData['R_xR'][j]
                    x_circ1_data = [circmean(allData['phi_xR'][j])]
                    y_circ1_data = np.mean(allData['R_xR'][j])

                elif k == 'Homolateral left("LF_LH")':
                    x_circ_data = allData['phi_xL'][j]
                    y_circ_data = allData['R_xL'][j]
                    x_circ1_data = [circmean(allData['phi_xL'][j])]
                    y_circ1_data = np.mean(allData['R_xL'][j])

                elif k == 'Contra-lateral frontleft-hindright("LF_RH")':
                    x_circ_data = allData['phi_fLhR'][j]
                    y_circ_data = allData['R_fLhR'][j]
                    x_circ1_data = [circmean(allData['phi_fLhR'][j])]
                    y_circ1_data = np.mean(allData['R_fLhR'][j])

                elif k == 'Contra-lateral frontright-hindleft("LH_RF")':
                    x_circ_data = allData['phi_fRhL'][j]
                    y_circ_data = allData['R_fRhL'][j]
                    x_circ1_data = [circmean(allData['phi_fRhL'][j])]
                    y_circ1_data = np.mean(allData['R_fRhL'][j])

                if not paperPlot:
                    fig = circularPlot(allData['phi'], allData['R'], fig, gs,
                                       gsNum=0, vNum=j)
                fig = circularPlot(x_circ_data, y_circ_data, fig,
                                   gs, gsNum=-1, vNum=j, paperPlot=paperPlot)

            # ax = fig.add_subplot(gs[0, :])

            # plt.title('Subject ' + f + ' .\n Left Cadence: %.2f Hz, Right Cadence: %.2f Hz, nSteps: %d\
            #                \n Using Avg. speed %.2f cm/s, Avg. left stride: %.2f cm, Avg. right stride: %.2f cm'
            #           % (np.mean(allData['lCad']), np.mean(allData['rCad']),
            #              sum(allData['nSteps']), np.mean(allData['avg']),
            #              np.mean(allData['lStLen']), np.mean(allData['rStLen'])))
            # for a in keys:
            #     allData[a] = np.hstack(allData[a])

                if not paperPlot:
                    fig = circularPlot([circmean(allData['phi'])],
                                       np.mean(allData['R']), fig, gs, gsNum=0, vNum=-1)

                fig = circularPlot(x_circ1_data, y_circ1_data,
                                   fig, gs, gsNum=-1, vNum=-1, paperPlot=paperPlot)

                #        pdb.set_trace()
                if k == 'Hindlimb("LH_RH")':
                    fig = cadencePlot(allData['movDur'][j], allData['lStride'][j],
                                      allData['rStride'][j], fig, gs, circPlot=False)

                elif k == 'Forelimb("LF_RF")':
                    fig = cadencePlot(allData['movDur'][j], allData['fRStride'][j],
                                  allData['fLStride'][j], fig, gs, circPlot=False)

                elif k == 'Homolateral right("RH_RF")':
                    fig = cadencePlot(allData['movDur'][j], allData['fRStride'][j],
                                      allData['rStride'][j], fig, gs, circPlot=False)

                elif k == 'Homolateral left("LF_LH")':
                    fig = cadencePlot(allData['movDur'][j], allData['fLStride'][j],
                                      allData['lStride'][j], fig, gs, circPlot=False)

                elif k == 'Contra-lateral frontleft-hindright("LF_RH")':
                    fig = cadencePlot(allData['movDur'][j], allData['fLStride'][j],
                                      allData['rStride'][j], fig, gs, circPlot=False)

                elif k == 'Contra-lateral frontright-hindleft("LH_RF")':
                    fig = cadencePlot(allData['movDur'][j], allData['fRStride'][j],
                                      allData['lStride'][j], fig, gs, circPlot=False)
                #        plt.legend()
                # plt.show()
                plt.title('Subject: ' + f.split('/')[-1] + '\n nSteps: %d \n Using Avg. speed %.2f cm/s' % (allData['nSteps'][j],allData['avg'][j]))
                # plt.savefig(f + '_' + k + '_' + str(j) + '.pdf')
                # list.append(fig)
                fig.clear()
    # return list

