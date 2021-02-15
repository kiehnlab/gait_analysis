from __future__ import division
from __future__ import print_function
import warnings
warnings.filterwarnings("ignore")

import time
import argparse
import pdb
import pickle
import os
#from coord import coordProfiler, meanVector, groupPlot
from coordination.constants import locKeys
import numpy as np
from coordination.plotter import processDict
import glob
import matplotlib.pyplot as plt
from pycircstat import watson_williams 
import itertools
from statsmodels.stats.multitest import multipletests
np.set_printoptions(precision=4,suppress=True)
from numpy import pi as PI
from stats import *

dirs = ['SOD1_study/',
       'CNO_study/',
       'SOD1-CNO_study/Pre-symptomatic_vs_onset/',
       'SOD1-CNO_study/SOD1-CNO_vs_before_after_CNO/']

## MAIN PROGRAM STARTS HERE ## 

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='/home/raghav/erda/Roser_project/Tracking/coordinationStudy/',
                    help='Path to coordination profiles')
parser.add_argument('--colors', type=str, default='',
                    help='Color schemes: sod,cno,both')
parser.add_argument('--steps', type=int, default='15',
                    help='Number of steps to use')
parser.add_argument('--seed', type=int, default=0,
                    help='Random seed')
parser.add_argument('--trial', type=int, default=1,
                    help='No. of random trials')
parser.add_argument('--alpha', type=float, default=0.05,
                    help='Significance threshold')
 
args = parser.parse_args()





for data_dir in dirs:
    np.random.seed(args.seed)
    if 'Pre-sym' in data_dir: # or '_CNO' in args.data:
        np.random.seed(400)
    print("\n#########################\nAnalyzing coordination for "\
          +data_dir+"\nUsing %d steps"%args.steps+\
          "\n#########################")
    data_dir = args.data+data_dir
    ### Process DLC tracks to obtain the speed profiles

#    pdb.set_trace()
    groups = list(set(glob.glob(data_dir+'*')) - set(glob.glob(data_dir+'*.pdf')))
    groups = sorted(groups)
    groupR = np.zeros(len(groups))
    groupPhi = np.zeros(len(groups))
    gNames = [g.split('/')[-1] for g in groups]
    gCombs = [[*x] for x in itertools.combinations(gNames,2)]
    if len(gCombs) == 6:
        gCombs = [gCombs[0],gCombs[-1]]
    saveLoc='/home/raghav/erda/Roser_project/Tracking/coordinationStudy/'
    keys =  ['h','xL','xR','fLhR','fRhL']
    for kIdx in range(len(keys)):
        key = keys[kIdx]
        print("\n#### Statistics for "+locKeys[kIdx]+" ####")
        for groups in gCombs:

            studyData = []
            for gIdx in range(len(groups)):
                g = groups[gIdx]
                files = sorted(glob.glob(data_dir+g+'/*.npy'))
                data = processDict(files)

                groupData = groupSteps(data,files,args.steps,key=key,T=args.trial)
                studyData.append(groupData)


            pVal = np.zeros(args.trial)
            for t in range(args.trial):
                if len(studyData) == 3:
                    pVal[t], table = watson_williams(studyData[0][t],studyData[1][t],studyData[2][t])
                elif len(studyData) == 4:
                    pVal[t], table = watson_williams(studyData[0][t],studyData[1][t],studyData[2][t],studyData[3][t])
                elif len(studyData) == 2:
                    pVal[t], table = watson_williams(studyData[0][t],studyData[1][t])

    #            print('Trial %d: p-value for groups '%(t)+groups[0]+' and '+groups[1]+': %.4f'%(pVal[t]))

    #        pdb.set_trace()
            levels, pAdj,_, p = multipletests(pVal,alpha=args.alpha)
            print("\nSignificance test for "+groups[0]+' and '+groups[1]+' with (p=%.4f)'%args.alpha)
    #        print("Before Bonferroni correction (p=%.4f)"%args.alpha)
            print(pVal,levels)
            if args.trial > 1:
                print("After Bonferroni correction:")# (p=%.4f)"%p)
                print(pAdj)
                print("%d/%d trials are significant"%(len(levels[levels==True]),args.trial))
#            print(levels)
