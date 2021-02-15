import pandas as pd
import numpy as np
import glob
import pyexifinfo as pex
import pdb
import warnings
warnings.filterwarnings("ignore")
import os
import matplotlib.pyplot as plt
from constants import *

def videoMetadata(vid):
    meta = {}
    meta['dur'] = np.float(pex.information(vid)['Composite:Duration'].replace(' s',''))
    meta['fps'] = np.int(pex.information(vid)['RIFF:VideoFrameRate'])
    meta['nFrame'] = nFrame = np.int(pex.information(vid)['RIFF:VideoFrameCount'])
    meta['imW']  = np.int(pex.information(vid)['RIFF:ImageWidth']) 
    meta['imH'] = np.int(pex.information(vid)['RIFF:ImageHeight'])
    meta['xPixW'] = length/meta['imW']

    print('Video of duration %.2f s with total %d frames, at %d fps and image size of %d x %d; each pixel is %.4f mm wide' \
          %(meta['dur'],meta['nFrame'],meta['fps'],meta['imW'],meta['imH'], meta['xPixW']))
    return meta

