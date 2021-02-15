from __future__ import division
from __future__ import print_function
import warnings
warnings.filterwarnings("ignore")
from stats import groupSteps
from constants import locKeys
import time
import argparse
import pdb
import pickle
import os
from coord import coordProfiler, meanVector, groupPlot
import numpy as np
from plotter import processDict
import glob
import matplotlib.pyplot as plt
import pandas as pd
import itertools
from pycircstat import watson_williams,kuiper
from scipy.stats import circmean
from astropy.stats import kuiper_two

np.random.seed(0)
## MAIN PROGRAM STARTS HERE ## 

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='/home/raghav/erda/kiehn_lab/nathalie/fasting_compressed/data/',
                    help='Path to coordination profiles')
parser.add_argument('--colors', type=str, default='',
                    help='Color schemes: sod,cno,both')
parser.add_argument('--steps', type=int, default='40',
                    help='Number of steps to use')
 
args = parser.parse_args()
print("Analyzing coordination from "+args.data)

### Process DLC tracks to obtain the speed profiles
groups = list(set(glob.glob(args.data+'*')) - set(glob.glob(args.data+'*.*')))
groups = sorted(groups)
groupR = np.zeros(len(groups))
groupPhi = np.zeros(len(groups))
gNames = [g.split('/')[-1].split('_')[0] for g in groups]
splits = pd.read_csv('data_split.txt',delimiter=',')
controls = splits[~splits.Control.isna()].Control.values
fasted = splits[~splits.Fasted.isna()].Fasted.values
splits = {'controls':controls,'fasted':fasted}
saveLoc= args.data.replace(args.data.split('/')[-2],'')[:-1]
#'/home/raghav/erda/Roser_project/Tracking/coordinationStudy/'
limbPairs = [['h'],['xL'],['xR'],['fLhR'],['fRhL']]
limbPair = 3
#pdb.set_trace()
pairName = locKeys[limbPair]
limbPair = limbPairs[limbPair]

speeds = ['20','30']
combs = [list(i) for i in itertools.product(gNames,splits.keys())] 
pairs = [list(i) for i in itertools.combinations(combs,2)]
idx = [0,1,3,6,8,9,10,13,14]
pairs = [ pairs[idx[i]] for i in range(len(idx))]
steps = [args.steps,args.steps+25]
s = -1
for speed in speeds:
    s += 1
    N = int(steps[s])
    for limbs in limbPair:
#        for gIdx in range(len(groups)):
        figNum = 0
        for pair in pairs:
            figNum += 1
            groupPhi = np.zeros(2)
            groupR = np.zeros(2)
            gNames = [p[0]+'_'+p[1] for p in pair]

            fig = plt.figure(figsize=(16,10))
            studyData = []
            for pIdx in range(2):
                g = pair[pIdx][0]
                split = pair[pIdx][1]
                files = []
                for f in splits[split]:
                    files=files+(sorted(glob.glob(args.data+\
                    g+'_compressed/'+f+'_compressed/allProfiles/*'+speed+'*.npy')))
                data = processDict(files)

#                pdb.set_trace()
                groupData = groupSteps(data,files,N)
                studyData.append(groupData)

#                fig = plt.figure(figsize=(16,10))
#                pdb.set_trace()
#                fig,groupPhi[gIdx],groupR[gIdx] = meanVector(data,files,fig,args.colors,gIdx,key=limbs)
#                plt.title(gNames[gIdx].replace('_',' ')+'_'+split)
#                plt.savefig(g+'/'+gNames[gIdx]+'_'+split+'_'+speed+'cms.pdf')

#            for gIdx in range(len(groups)):
#                g = groups[gIdx]
#                files = sorted(glob.glob(g+'/*.npy'))
#                data = processDict(files)
#                pdb.set_trace()
                fig,groupPhi[pIdx],groupR[pIdx] = meanVector(data,files,fig,
                                                         args.colors,gNames[pIdx],key=limbs,scatter=True)
        #    plt.title(gNames[gIdx].replace('_',' '))
        #    plt.savefig(g+'.pdf')

            populations = []
            for i in range(len(studyData)):
                tmp = [circmean(studyData[i][0,j]) for j in range(studyData[i].shape[1])]
                populations.append(tmp)

#            pdb.set_trace()
#            pVal, table = watson_williams(studyData[0].reshape(-1),studyData[1].reshape(-1))
            pVal, table = watson_williams(populations[0],populations[1])
#            pVal, table = kuiper(np.array(populations[0]),np.array(populations[1]))

            print(gNames,speed,pVal)

            fig,meanPhi,meanR = groupPlot(groupPhi,groupR,fig,gNames) #,day=g,group=split)
            plt.title(pairName+' '+gNames[0]+' vs '+gNames[1]+'  p=%.4f, N= %d, '%(pVal,N)+speed+' cm/s') 
            plt.legend()
        #    pdb.set_trace()
            plt.savefig(saveLoc+args.data.split('/')[-2]+'/'+\
                        pairName+'_'+speed+'cms_'+gNames[0]+'_vs_'+gNames[1]+'.pdf')


