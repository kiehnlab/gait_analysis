from __future__ import division
from __future__ import print_function
import warnings
warnings.filterwarnings("ignore")

import time
import argparse
import pdb
import pickle
import os
os.environ['DLClight'] = 'True'
from profiler import locomotionProfiler
from plotter import combinedPlot
import shutil
import glob

## MAIN PROGRAM STARTS HERE ## 

parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, 
                    default='/home/jwg356/erda/Roser_project/Tracking/DLC_model/config.yaml',
                    help='Path to config files')
parser.add_argument('--data', type=str, default='/home/raghav/erda/Roser_project/Tracking/',
                    help='Path to video files.')
parser.add_argument('--analyze_video', action='store_true', default=False,
                    help='Analyze videos.')
parser.add_argument('--label_video', action='store_true', default=False,
                    help='Make labelled videos.')

args = parser.parse_args()
if args.analyze_video or args.label_video:
    import deeplabcut
print("Using config file:"+args.config)
print("Analyzing videos in location"+args.data)
if args.data[-1] != '/':
    args.data = args.data+'/'
dest = args.data+'labels/'
if os.path.exists(dest):
    if args.analyze_video:
        print("Found directory with labels... Overwriting them....")
        shutil.rmtree(dest) 
        os.mkdir(dest)
else:
     os.mkdir(dest)

### Step:1 
### Use trained DeepLabCut model to obtain tracks for markers
if args.analyze_video:
    deeplabcut.analyze_videos(args.config,[args.data],videotype='.avi',destfolder=args.data)
if args.label_video:
    labvid_dir=args.data+'labeled_videos'
    if os.path.exists(labvid_dir):
        print("Found directory with labelled videos... Overwriting them....")
        shutil.rmtree(labvid_dir) 
    os.mkdir(labvid_dir)
        
    deeplabcut.create_labeled_video(args.config,[args.data],videotype='.avi')
    labels=glob.glob(args.data+'*labeled.mp4')
    [shutil.move(f,labvid_dir) for f in labels]
   
if args.analyze_video:
    labels=glob.glob(args.data+'*.h5')
    [shutil.move(f,dest) for f in labels]
    labels=glob.glob(args.data+'*.pickle')
    [shutil.move(f,dest) for f in labels]

### Step:2
### Process DLC tracks to obtain all measurements
locomotionProfiler(data_path=dest,saveFlag=True, plotFlag=True, log=True)

### Step:3
### Process DLC tracks to obtain the speed profiles
combinedPlot(data_path=args.data+'allProfiles/',saveFlag=True,paperPlot=True)


