import pandas as pd
import numpy as np
import glob
import pyexifinfo as pex
import pdb
import warnings
warnings.filterwarnings("ignore")
import os
import matplotlib.pyplot as plt
from gait_analysis.coordination.constants import *
#from coordination.constants import *

def processDict(dFiles,phiThresh=0):
    allData = allData=dict.fromkeys(keys,[])

    for dFname in dFiles:
        data = np.load(dFname,allow_pickle=True).item()
        ### Choose diagonal steps that are similar
        if phiThresh > 0:
            idx = np.where(np.abs(data['phi_fRhL']-data['phi_fLhR']) < phiThresh)[0]
            data['phi_fRhL'] = data['phi_fRhL'][idx]
            data['phi_fLhR'] = data['phi_fLhR'][idx]
            data['phi_xL'] = data['phi_xL'][idx]
            data['phi_xR'] = data['phi_xR'][idx]
            data['phi_h'] = data['phi_h'][idx]
            data['phi_f'] = data['phi_f'][idx]

        for key,value in data.items():
            allData[key] = allData[key]+[value]

    return allData

def videoMetadata(vid):
    meta = {}
    time_str = pex.information(vid)['Composite:Duration']

    if ' s' in time_str:
        meta['dur'] = np.float(time_str.replace(' s',''))
    else:
        ftr = [3600,60,1]
        meta['dur'] = np.float(sum([a*b for a,b in zip(ftr, map(int,time_str.split(':')))]))/5
    meta['fps'] = np.int(pex.information(vid)['RIFF:VideoFrameRate'])*5
    meta['nFrame'] = nFrame = np.int(pex.information(vid)['RIFF:VideoFrameCount'])
    meta['imW']  = np.int(pex.information(vid)['RIFF:ImageWidth']) 
    meta['imH'] = np.int(pex.information(vid)['RIFF:ImageHeight'])
    meta['xPixW'] = length/meta['imW']

    print('Video of duration %.2f s with total %d frames, at %d fps and image size of %d x %d; each pixel is %.4f mm wide' \
          %(meta['dur'],meta['nFrame'],meta['fps'],meta['imW'],meta['imH'], meta['xPixW']))
    return meta

#{'SourceFile': '/home/janek/Documents/Jan-try-2021-02-17/SIDEVIEW_Cage1_0L0R_20cms_0degUP_4.mp4', 'ExifTool:ExifToolVersion': 10.8, 'File:Directory': '/home/janek/Documents/Jan-try-2021-02-17', 'File:FileAccessDate': '2021:02:18 16:06:44+01:00', 'File:FileInodeChangeDate': '2021:02:18 16:06:30+01:00', 'File:FileModifyDate': '2021:02:18 15:58:34+01:00', 'File:FileName': 'SIDEVIEW_Cage1_0L0R_20cms_0degUP_4.mp4', 'File:FilePermissions': 'rw-r--r--', 'File:FileSize': '1037 kB', 'File:FileType': 'MP4', 'File:FileTypeExtension': 'mp4', 'File:MIMEType': 'video/mp4', 'QuickTime:BitDepth': 24, 'QuickTime:CompatibleBrands': ['mp41', 'avc1'], 'QuickTime:CompressorID': 'mp4v', 'QuickTime:CreateDate': '2021:02:18 14:25:42', 'QuickTime:CurrentTime': '0 s', 'QuickTime:Duration': '2.10 s', 'QuickTime:GraphicsMode': 'srcCopy', 'QuickTime:HandlerDescription': 'VideoHandler', 'QuickTime:HandlerType': 'Video Track', 'QuickTime:ImageHeight': 296, 'QuickTime:ImageWidth': 658, 'QuickTime:MajorBrand': 'MP4  Base Media v1 [IS0 14496-12:2003]', 'QuickTime:MatrixStructure': '1 0 0 0 1 0 0 0 1', 'QuickTime:MediaCreateDate': '2021:02:18 14:25:42', 'QuickTime:MediaDuration': '2.10 s', 'QuickTime:MediaHeaderVersion': 0, 'QuickTime:MediaModifyDate': '2021:02:18 14:25:42', 'QuickTime:MediaTimeScale': 90000, 'QuickTime:MinorVersion': '0.0.0', 'QuickTime:ModifyDate': '2021:02:18 14:25:42', 'QuickTime:MovieDataOffset': 2617, 'QuickTime:MovieDataSize': 1059116, 'QuickTime:MovieHeaderVersion': 0, 'QuickTime:NextTrackID': 2, 'QuickTime:OpColor': '0 0 0', 'QuickTime:PosterTime': '0 s', 'QuickTime:PreferredRate': 1, 'QuickTime:PreferredVolume': '100.00%', 'QuickTime:PreviewDuration': '0 s', 'QuickTime:PreviewTime': '0 s', 'QuickTime:Requirements': 'QuickTime 6.0 or greater', 'QuickTime:SelectionDuration': '0 s', 'QuickTime:SelectionTime': '0 s', 'QuickTime:SourceImageHeight': 296, 'QuickTime:SourceImageWidth': 658, 'QuickTime:TimeScale': 90000, 'QuickTime:TrackCreateDate': '2021:02:18 14:25:42', 'QuickTime:TrackDuration': '2.10 s', 'QuickTime:TrackHeaderVersion': 0, 'QuickTime:TrackID': 1, 'QuickTime:TrackLayer': 0, 'QuickTime:TrackModifyDate': '2021:02:18 14:25:42', 'QuickTime:TrackVolume': '0.00%', 'QuickTime:UserData_enc': 'vlc 3.0.12.1 stream output', 'QuickTime:VideoFrameRate': 152, 'QuickTime:XResolution': 72, 'QuickTime:YResolution': 72, 'Composite:AvgBitrate': '4.04 Mbps', 'Composite:ImageSize': '658x296', 'Composite:Megapixels': 0.195, 'Composite:Rotation': 0}

def select_animals(group,button):

    cwd = os.getcwd()
    dlg = wx.FileDialog(
        self, "Select animals for the current group", cwd, "", "*.*", wx.FD_MULTIPLE
    )
    if dlg.ShowModal() == wx.ID_OK:
        vids = dlg.GetPaths()
        new_vids = []
        for i in vids:
            if i in group:
                continue
            else:
                new_vids.append(i)
        group = group + new_vids
        button.SetLabel("Total %s Animals selected for current group" % len(group))
    return group
