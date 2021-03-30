from __future__ import division
from __future__ import print_function
import warnings
warnings.filterwarnings("ignore")
#from gait_analysis.coordination.stats import groupSteps
#from gait_analysis.coordination.constants import locKeys
# from coordination.stats import groupSteps
# from coordination.constants import locKeys
import time
import argparse
import pdb
import pickle
import os
#from gait_analysis.coordination.coord import coordProfiler, meanVector, groupPlot
# from coordination.coord import coordProfiler, meanVector, groupPlot
import numpy as np
#from gait_analysis.coordination.plotter import processDict
# from coordination.plotter import processDict
import glob
import matplotlib.pyplot as plt
import pandas as pd
import itertools
# from pycircstat import watson_williams,kuiper
# from scipy.stats import circmean
# from astropy.stats import kuiper_two

from gait_analysis.coordination.stats import *
from gait_analysis.coordination.tools import processDict
from gait_analysis.coordination.constants import *
from gait_analysis.coordination.coord import *

colors = ['salmon','mediumorchid','deepskyblue','darkorange']
data = '/home/janek/Desktop/Jan-group-2021-03-23/'
def Group_profiler(groups,names,stride,n_steps,phi_thr,test):

    groups_final = []
    for i in groups:
        if len(i) > 0:
        #     if len(i) == 1:
        #         groups.append()
            groups_final.append(i)

    path_labels = '/'.join(groups_final[0][0].split('/')[:-1]) + '/allProfiles/'
    with open(path_labels + 'stats.txt', 'w') as f:
        print('Limb coordination: \t Pair \t Statistical test \t p-value \t Number of steps \t Belt speed ', file=f)





    # names = [name_group1,name_group2,name_group3,name_group4]
    names_final = []
    for i in names:
        if len(i) != 0:
            names_final.append(i)

    combs = []
    for i in itertools.combinations(names,2):
        i = list(i)
        if len(i[0]) == 0:
        #     print(i)
            continue
        elif len(i[1]) == 0:
            continue
        else:
            combs.append(i)
    # combs = [c[0]+'_'+c[1] for c in combs]


    # print(groups_final)
    # print(names_final)
    # print(combs)

    phi = 0.5
    allData = {}
    N = n_steps
    for i in range(len(names_final)):
        labels = []
        for f in groups_final[i]:
            l = f.replace('.avi','*.npy')
            labels = labels + sorted(glob.glob(path_labels + l.split('/')[-1]))
        data = processDict(labels, phiThresh=phi_thr)
        allData[names_final[i]] = groupSteps(data,labels, N)



    for j in stride:
        # plt.clf()
        fig = plt.figure(figsize=(16, 12))

        allGroupPhi = np.zeros(len(names_final))
        allGroupR = np.zeros(len(names_final))

        for i in range(len(names_final)):
            groupData = allData[names_final[i]][j]
            # pdb.set_trace()
            fig,allGroupPhi[i],allGroupR[i] = meanVector(groupData,labels,fig,colors[i],names_final[i],idx=j,
                                                         scatter=True)
        # pdb.set_trace()
        # fig = groupPlot(allGroupPhi,allGroupR,fig,names_final,colors)
        ax = fig.add_subplot(111, polar=True)
        ax.set_rlim(0, 1.1)
        ax.spines['polar'].set_visible(False)
        # ax.set_axisbelow(True)
        ax.set_theta_offset(np.pi / 2)
        ax.grid(linewidth=2,visible=True)
        plt.legend()
        plt.savefig(path_labels+locKeys[j]+'.pdf')

        for comb in combs:
            studyData = []
            # g = comb.split('_')[0]
            # h = comb.split('_')[1]
            # f = [g,h]
            # pdb.set_trace()
            for pIdx in range(2):
                groupData = allData[comb[pIdx]][j]
                studyData.append(groupData)

            populations = []
            for i in range(len(studyData)):
                tmpPhi = [circular_mean(studyData[i][k])[0] for k in range(studyData[i].shape[0])]
                tmpR = [circular_mean(studyData[i][k])[1] for k in range(studyData[i].shape[0])]
                tmp = [tmpPhi, tmpR]
                populations.append(tmp)
            # print(populations)
            if test == 'Modified Rayleigh test':
                pVal, table = modified_rayleigh(populations[0][0], populations[0][1],
                                                populations[1][0], populations[1][1])
                if pVal < 0.001:
                    sig = '***'
                elif pVal < 0.05:
                    sig = '*'
                else:
                    sig = 'n.s'
                string = (locKeys[j] + '\t' + comb[0] + ' vs ' + comb[1] + '\tMod. Rayleigh\tp=%.4f' % (
                    pVal) + ' (' + sig + ')\tN = %d\t' % (N) + '20' + 'cm/s')
                with open(path_labels + 'stats.txt', 'a') as f:
                    print(string, file=f)
            # print(string)
            elif test == 'Watson-Williams test':
                pVal, table = watson_williams(populations[0][0], populations[1][0])
                if pVal < 0.001:
                    sig = '***'
                elif pVal < 0.05:
                    sig = '*'
                else:
                    sig = 'n.s'
                string = (locKeys[j] + '\t' + comb[0] + ' vs ' + comb[1] + '\tWatson-Williams\tp=%.4f' % (
                    pVal) + ' (' + sig + ')\tN = %d\t' % (N) + '20' + 'cm/s')
                with open(path_labels + 'stats.txt', 'a') as f:
                    print(string, file=f)
            # print(string)
            else:
                pVal, table = modified_rayleigh(populations[0][0], populations[0][1],
                                                populations[1][0], populations[1][1])
                if pVal < 0.001:
                    sig = '***'
                elif pVal < 0.05:
                    sig = '*'
                else:
                    sig = 'n.s'
                string1 = (locKeys[j] + '\t' + comb[0] + ' vs ' + comb[1] + '\tMod. Rayleigh\tp=%.4f' % (
                    pVal) + ' (' + sig + ')\tN = %d\t' % (N) + '20' + 'cm/s')

                pVal, table = watson_williams(populations[0][0], populations[1][0])
                if pVal < 0.001:
                    sig = '***'
                elif pVal < 0.05:
                    sig = '*'
                else:
                    sig = 'n.s'

                string2 = (locKeys[j] + '\t' + comb[0] + ' vs ' + comb[1] + '\tWatson-Williams\tp=%.4f' % (
                    pVal) + ' (' + sig + ')\tN = %d\t' % (N) + '20' + 'cm/s')
                with open(path_labels + 'stats.txt', 'a') as f:
                    print(string1 + '\n' + string2, file=f)





# np.random.seed(0)
# ## MAIN PROGRAM STARTS HERE ##
#
# parser = argparse.ArgumentParser()
# parser.add_argument('--data', type=str, default='/home/raghav/erda/kiehn_lab/nathalie/fasting_compressed/data/',
#                     help='Path to coordination profiles')
# parser.add_argument('--colors', type=str, default='',
#                     help='Color schemes: sod,cno,both')
# parser.add_argument('--steps', type=int, default='40',
#                     help='Number of steps to use')
#
# args = parser.parse_args()
# print("Analyzing coordination from "+args.data)
#
# ### Process DLC tracks to obtain the speed profiles
# groups = list(set(glob.glob(args.data+'*')) - set(glob.glob(args.data+'*.*')))
# groups = sorted(groups)
# groupR = np.zeros(len(groups))
# groupPhi = np.zeros(len(groups))
# gNames = [g.split('/')[-1].split('_')[0] for g in groups]
# splits = pd.read_csv('data_split.txt',delimiter=',')
# controls = splits[~splits.Control.isna()].Control.values
# fasted = splits[~splits.Fasted.isna()].Fasted.values
# splits = {'controls':controls,'fasted':fasted}
# saveLoc= args.data.replace(args.data.split('/')[-2],'')[:-1]
# #'/home/raghav/erda/Roser_project/Tracking/coordinationStudy/'
# limbPairs = [['h'],['xL'],['xR'],['fLhR'],['fRhL']]
# limbPair = 3
# #pdb.set_trace()
# pairName = locKeys[limbPair]
# limbPair = limbPairs[limbPair]
#
# speeds = ['20','30']
# combs = [list(i) for i in itertools.product(gNames,splits.keys())]
# pairs = [list(i) for i in itertools.combinations(combs,2)]
# idx = [0,1,3,6,8,9,10,13,14]
# pairs = [ pairs[idx[i]] for i in range(len(idx))]
# steps = [args.steps,args.steps+25]
# s = -1
# for speed in speeds:
#     s += 1
#     N = int(steps[s])
#     for limbs in limbPair:
# #        for gIdx in range(len(groups)):
#         figNum = 0
#         for pair in pairs:
#             figNum += 1
#             groupPhi = np.zeros(2)
#             groupR = np.zeros(2)
#             gNames = [p[0]+'_'+p[1] for p in pair]
#
#             fig = plt.figure(figsize=(16,10))
#             studyData = []
#             for pIdx in range(2):
#                 g = pair[pIdx][0]
#                 split = pair[pIdx][1]
#                 files = []
#                 for f in splits[split]:
#                     files=files+(sorted(glob.glob(args.data+\
#                     g+'_compressed/'+f+'_compressed/allProfiles/*'+speed+'*.npy')))
#                 data = processDict(files)
#
# #                pdb.set_trace()
#                 groupData = groupSteps(data,files,N)
#                 studyData.append(groupData)
#
# #                fig = plt.figure(figsize=(16,10))
# #                pdb.set_trace()
# #                fig,groupPhi[gIdx],groupR[gIdx] = meanVector(data,files,fig,args.colors,gIdx,key=limbs)
# #                plt.title(gNames[gIdx].replace('_',' ')+'_'+split)
# #                plt.savefig(g+'/'+gNames[gIdx]+'_'+split+'_'+speed+'cms.pdf')
#
# #            for gIdx in range(len(groups)):
# #                g = groups[gIdx]
# #                files = sorted(glob.glob(g+'/*.npy'))
# #                data = processDict(files)
# #                pdb.set_trace()
#                 fig,groupPhi[pIdx],groupR[pIdx] = meanVector(data,files,fig,
#                                                          args.colors,gNames[pIdx],key=limbs,scatter=True)
#         #    plt.title(gNames[gIdx].replace('_',' '))
#         #    plt.savefig(g+'.pdf')
#
#             populations = []
#             for i in range(len(studyData)):
#                 tmp = [circmean(studyData[i][0,j]) for j in range(studyData[i].shape[1])]
#                 populations.append(tmp)
#
# #            pdb.set_trace()
# #            pVal, table = watson_williams(studyData[0].reshape(-1),studyData[1].reshape(-1))
#             pVal, table = watson_williams(populations[0],populations[1])
# #            pVal, table = kuiper(np.array(populations[0]),np.array(populations[1]))
#
#             print(gNames,speed,pVal)
#
#             fig,meanPhi,meanR = groupPlot(groupPhi,groupR,fig,gNames) #,day=g,group=split)
#             plt.title(pairName+' '+gNames[0]+' vs '+gNames[1]+'  p=%.4f, N= %d, '%(pVal,N)+speed+' cm/s')
#             plt.legend()
#         #    pdb.set_trace()
#             plt.savefig(saveLoc+args.data.split('/')[-2]+'/'+\
#                         pairName+'_'+speed+'cms_'+gNames[0]+'_vs_'+gNames[1]+'.pdf')


