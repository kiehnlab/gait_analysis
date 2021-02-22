import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import time
import os
from coordination.plotter import *
from coordination.tools import videoMetadata
from coordination.constants import *
import pdb
from scipy.stats import circmean
from coordination.coord import iqrMean, heurCircular
from matplotlib import gridspec
from coordination.accel import estimateAccel, analyseDragRec
import pyexifinfo as pex

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
from coordination.tools import videoMetadata
from coordination.constants import *
from coordination.accel import *
from coordination.coord import bodyPosCoord, bodyCoordCircular, circularPlot, cadencePlot


def accel_plotter(project_path,start=0,end=-1):
    os.chdir(project_path)
    files = sorted(glob.glob('*.avi'))
    files = [f.replace('.avi', '') for f in files]
    videoName = project_path.split('/')[-1].replace('_', ' ')
    print(files)
    print(videoName)
    for ipFile in files:
        meta = videoMetadata(ipFile + '.avi')
        sFrame = 0
        eFrame = meta['nFrame']

        if not os.path.exists('overlays'):
            os.mkdir('overlays')

        filename = sorted(glob.glob('labeled_videos/' + ipFile + '*_labeled.mp4'))[0]

        dataFiles = sorted(glob.glob('allProfiles/' + ipFile + '*_Profile.npy'))

        allData = processDict(dataFiles)

        ### Obtain speed parameters
        speedAll = allData['speed'][0]
        speedMean = speedAll.mean(0)
        speedMean = np.convolve(speedMean,
                                np.ones((speedSmFactor,)) / speedSmFactor, mode='valid')
        speedStd = speedAll.std(0)
        speedStd = np.convolve(speedStd,
                               np.ones((speedSmFactor,)) / speedSmFactor, mode='valid')


        newFrame = speedMean.shape[0]
        yMax = (speedMean + speedStd).max()  # + speedStd.max()
        yMin = (speedMean - speedStd).min()
        avgSpeed = speedMean[::int(meta['fps'] / 3)].mean()


        ### Obtain cadence parameters
        lStride = allData['lStride'][0]
        rStride = allData['rStride'][0]
        lSMean = iqrMean(lStride)
        rSMean = iqrMean(rStride)
        sMean = lSMean - rSMean
        stride = lStride - rStride
        sMin = stride.min()
        sMax = stride.max()
        T = len(lStride)

        #        pdb.set_trace()
        if start > 0:
            idx = int(start / meta['dur'] * newFrame)
            speedMean = speedMean[idx:]
            speedStd = speedStd[idx:]

            idx = int(start / meta['dur'] * T)
            stride = stride[idx:]
            sFrame = int(start / meta['dur'] * meta['nFrame'])

        if end > -1:
            idx = newFrame - int(end / meta['dur'] * newFrame)
            speedMean = speedMean[:-idx]
            speedStd = speedStd[:-idx]

            idx = T - int(end / meta['dur'] * T)
            stride = stride[:-idx]
            eFrame = int(end / meta['dur'] * meta['nFrame'])

        if start > 0 or end > -1:

            newFrame = speedMean.shape[0]
            T = len(stride)
            dur = end - start
            phi, R, _, _, idx = heurCircular(np.arange(T), stride, sMean, True)
            xAxis = np.linspace(0, dur, newFrame)
            cAxis = np.linspace(0, dur, T)

        else:
            ### Obtain circular plot parameters
            phi = allData['phi_h'][0]
            R = allData['R_h'][0]
            idx = np.where(np.diff(stride > sMean) == True)[0]
            dur = meta['dur']

            xAxis = np.linspace(0, meta['dur'], newFrame)
            cAxis = np.linspace(0, meta['dur'], T)

        if len(idx) % 2 != 0:
            idx = idx[:-1]
        idx = idx.reshape(-1, 2)[:, 0]


               #pdb.set_trace()
        # Perform acceleration analysis
        accMean, drgIdx, recIdx, _ = estimateAccel(speedMean, meta)
        dragCount, recCount, drgDur, recDur, drgIdx, recIdx = \
            analyseDragRec(drgIdx, recIdx, meta['fps'], tThr)
        aAxis = np.linspace(0, dur, accMean.shape[0])
        #
        print("Drag events: %d, Rec. events : %d" % (dragCount, recCount))

        plotDragReco(aAxis,accMean,drgIdx,recIdx,dragCount,recCount,drgDur,recDur,ipFile,True)



