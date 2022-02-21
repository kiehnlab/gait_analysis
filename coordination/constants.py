# Global parameters

#model name
model = 'DLC_resnet50_MultipleMarkersNov15shuffle1_4500'
model_lateral = 'DLC_resnet_50_lateral_analysisOct26shuffle1_100000'

# Marker ids used in DeepLabCut
mrkr = ['snout', 'snoutL', 'snoutR', 'foreL', 'foreR','hindL', 
                'hindR', 'torso', 'torsoL', 'torsoR', 'tail']
# Markers used in speed estimation. Excludes paws which are used in coordination
speedMarkers = ['tail','snout', 'snoutL', 'snoutR', 'torso', 'torsoL', 'torsoR']
length = 220 # Width of the image in mm
# Time points
time_points = range(49,115,7)
time_points = ['P'+repr(i) for i in time_points ]

# Smoothing window for position estimates
smFactor = 1
# Smoothing window for speed estimates
#speedSmFactor = 10
speedThr = 5 # Used to leave out stride and cadence calcuations
# Acceleration smoothing params
#tThr = 0.25 # Duration to count a drag/recovery event
accSmFactor = 12
# Location to save speedProfiles
spProfLoc = '../allProfiles'
#spProfLoc = '../speedProfile'
acProfLoc = '../accelProfile'
cdProfLoc = '../coordProfile'

# Interpolation factor
INTERP = 4

# Keys for archive
keys=['speed','lCad','rCad','flCad','frCad','avg','rStLen','lStLen',
      'frStLen','flStLen','phi','R','nSteps','phi_h','R_h','phi_f','R_f','phi_xR','R_xR',
      'phi_xL','R_xL', 'phi_fLhR', 'R_fLhR','phi_fRhL','R_fRhL',
      'movDur',  'rStride','lStride','fRStride','fLStride']
colors=['black','blue','green','grey']
legends=['1st','2nd','3rd','Mean']
locKeys = ['LH_RH','LF_RF','LH_LF','RH_RF','LF_RH','RF_LH']
limbPairs = ['h','f','xL','xR','fLhR','fRhL']

## For making video overlays
frameRate = 24

df_cols = ['name', 'bodyLen', 'duration','belt speed','avg.speed',\
        'loc_front', 'loc_rear', 'peak_acc','num_drag',\
        'num_rec','count_ratio','dur_drag','dur_rec','mov_dur','num_steps',\
        'LH_st_len','LF_st_len','RH_st_len','RF_st_len',\
        'LH_st_frq','LF_st_frq','RH_st_frq','RF_st_frq',\
        'LHRH_ang','LHLF_ang','RHRF_ang','LFRH_ang','RFLH_ang','LFRF_ang',\
        'LHRH_rad','LHLF_rad','RHRF_rad','LFRH_rad','RFLH_rad','LFRF_rad',\
        'hip_ang','knee_ang','ankle_ang','foot_ang'
        ]
