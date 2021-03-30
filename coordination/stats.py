from __future__ import division
from __future__ import print_function
import warnings
import time
import argparse
import pdb
import pickle
import os
#from coord import coordProfiler, meanVector, groupPlot
from gait_analysis.coordination.constants import locKeys,limbPairs
import numpy as np
from gait_analysis.coordination.tools import processDict
import glob
import matplotlib.pyplot as plt
from pycircstat import watson_williams 
from scipy.stats import circmean
import itertools
from statsmodels.stats.multitest import multipletests
from numpy import pi as PI
np.set_printoptions(precision=4,suppress=True)
warnings.filterwarnings("ignore")

def rCDF(r,N):
    return np.exp(-(6 * r**2 * N**2)/((N+1)*(2*N+1)))

def modified_rayleigh(phi1, r1, phi2, r2):
    """
    Transform the directional data based on weights derived from 
    concentration parameter.
    See: A modification of the Rayleigh test for vector data. Bruce Moore 1980
    return pval, statistic R (Eq.3.1)
    """
    X1 = r1 * np.cos(phi1)
    Y1 = r1 * np.sin(phi1)
    N1 = len(r1)
    X2 = r2 * np.cos(phi2)
    Y2 = r2 * np.sin(phi2)
    N2 = len(r2)

    if N1 != N2:
        if N1 > N2:
            X2 = np.concatenate((X2,X2[:(N1-N2)]))
            Y2 = np.concatenate((Y2,Y2[:(N1-N2)]))
        else:
            X1 = np.concatenate((X1,X1[:(N2-N1)]))
            Y1 = np.concatenate((Y1,Y1[:(N2-N1)]))

    dX = X1-X2
    dY = Y1-Y2
    r = np.sqrt(dX**2 +dY**2)
    N = len(r)
    phi = np.arctan2(dY,dX)
    rank = np.argsort(r) + 1
    X = np.sum(rank * np.cos(phi))
    Y = np.sum(rank * np.sin(phi))
    R = np.sqrt(X**2 + Y**2)
    R_ = R/ N**(1.5)

    pval = rCDF(R_,N) 

    return pval, R_

def circular_mean(phi,r=np.ones(1),ignore_zeros=True):
    # if ignore_zeros:
    #     phi = phi[phi != 0]
    #     if len(r) != 1:
    #         r = r[phi != 0]
    # X = (r*np.cos(phi)).mean()
    # Y = (r*np.sin(phi)).mean()
    # meanR = np.sqrt(X**2+Y**2)
    # meanPhi = np.arctan2(Y,X)
    # return meanPhi, meanR
    X = np.cos(phi).mean()
    Y = np.sin(phi).mean()
    meanR = np.sqrt(X**2+Y**2)
    meanPhi = np.arctan2(Y,X)
    return meanPhi, meanR

def densitySample(phi,N,bins=36):
    """
    Sample steps matching the actual distribution
    Assumes angles in degrees
    """
    binRange = np.arange(0,361,360//(bins))
    phi = phi * 180/np.pi
    phi = phi[np.random.permutation(len(phi))]
    pdf, levels = np.histogram(phi,bins=binRange)
#    levels = np.concatenate((levels.reshape(-1),np.array([levels.sum()])))

    pdf = pdf/pdf.sum()
    stepDist = (np.round(pdf*N)).astype(int)
    if stepDist.sum() != N:
        stepDist[np.argmax(stepDist)] -= (stepDist.sum()-N)
    phiSample = np.zeros(1)
    for l in range(bins):
        if stepDist[l] > 0:
            samples = phi[(phi > levels[l]) & (phi <= levels[l+1])]
            samples = samples[:stepDist[l]]
            phiSample = np.concatenate((phiSample,samples.reshape(-1)))
    
    return phiSample[-N:]*np.pi/180

def medianSamples(phi,N):
    """
    Sample steps matching the distribution on either side of median angle
    Use median step angle and sample N/2 on either side
    """
#    pdb.set_trace()
#    phi = phi[np.random.permutation(len(phi))]
    phi = np.sort(phi)
    medAng = np.median(phi)
    lIdx = (phi >= medAng) 
    lPhi = phi[lIdx]#[::-1]
    uPhi = phi[~lIdx][::-1]
    phi = np.concatenate((uPhi[:N//2],lPhi[:N//2+1]))
    phiRet = np.zeros(N)
    phiRet[:len(phi)] = phi
    return phiRet

def tailSamples(phi,phi_h,N):
    """
    Exclude majority samples assuming they concentrate 
    around PI. Use hind limb for choosing steps
    """
#    pdb.set_trace()
    tmp = (phi_h/2 - np.pi/2)
    idx = np.argsort(tmp)
    phi = phi[idx[-N:]]
    return phi 

def sampleSteps(phi,N,discrete=False):
    """
    Sample steps matching the distribution between the upper and lower
    halves of the circle
    Use median step angle and sample N/2 on either side
    """
    if discrete:
        phi = phi/PI*180
        phi = phi + (30 - phi % 30)
        phi = phi/180*PI
#    pdb.set_trace()
    phi = phi[np.random.permutation(len(phi))]
    lIdx = (phi >= PI/2) & (phi <= 3*PI/2)
    lPhi = phi[lIdx]
    uPhi = phi[~lIdx]
    if len(lPhi) >= len(uPhi):
        ratio = int(np.ceil(N*(len(uPhi)+1)/(len(lPhi)+1)-1))
        phi = np.concatenate((uPhi[:ratio],lPhi[:(N-uPhi[:ratio].shape[0])]))
    else:
#        pdb.set_trace()
        ratio = int(np.ceil(N*(len(lPhi)+1)/(len(uPhi)+1)-1))
        phi = np.concatenate((lPhi[:ratio],uPhi[:(N-lPhi[:ratio].shape[0])]))
    phiRet = np.zeros(N)
    phiRet[:len(phi)] = phi
    return phiRet

def groupSteps(data,files,nSteps,key='h',T=6,bins=36):
    # files = np.array([f.split('/')[-1][:20] for f in files])
    # uniq = np.unique(files)
    N = len(files)
    groupData = np.zeros((T,N,nSteps))
    #pdb.set_trace()
    for t in range(T):
        for i in range(len(files)):
            # idx = list(np.argwhere(files==files[i]).reshape(-1))
            # animSteps = np.zeros((nSteps,len(idx)))
            # for aIdx in range(len(idx)):
            #     anim = idx[aIdx]
#                aSteps = tailSamples(data['phi_'+key][anim],\
#                        data['phi_h'][anim], nSteps)
                #pdb.set_trace()
            aSteps = data['phi_'+limbPairs[t]][i]
            if len(aSteps) >= nSteps:
                aSteps = aSteps[:nSteps]
            # animSteps[:len(aSteps),aIdx] = aSteps
#            pdb.set_trace()
#             animSteps = animSteps.reshape(-1)
#             animSteps = animSteps[animSteps != 0]
#             pdb.set_trace()
            nA = len(aSteps)
            if nA <= nSteps: #or nA <= bins:
                if nA < nSteps:
                    nSteps = nA
                    print("Using %d steps"%nSteps)
            groupData[t,i,:nSteps] = aSteps[:nSteps]

#                groupData[t,i,:nSteps] = densitySample(animSteps,nSteps,bins) 
#             groupData[t,i,:nSteps] = aSteps[:nSteps]
#                groupData[t,i,:nSteps] = tailSamples(animSteps,nSteps)
#                groupData[t,i,:nSteps] = animSteps[np.random.permutation(len(animSteps))][:nSteps]
                
    return groupData

def groupAllSteps(data,files,nSteps,T=5,bins=36):
    files = np.array([f.split('/')[-1][:20] for f in files])
    uniq = np.unique(files)
    N = len(uniq)
    groupData = np.zeros((T,N,nSteps))

#    limbPairs = ['h','xL','xR','fLhR','fRhL'] -> T:[0,1,2,3,4]

    for t in range(T):
        for i in range(len(uniq)):
            idx = list(np.argwhere(files==uniq[i]).reshape(-1))
            animSteps = np.zeros((nSteps,len(idx)))
            for aIdx in range(len(idx)):
                anim = idx[aIdx]
                aSteps = tailSamples(data['phi_'+limbPairs[t]][anim],\
                        data['phi_h'][anim], nSteps)
#                pdb.set_trace()
                animSteps[:len(aSteps),aIdx] = aSteps
            animSteps = animSteps.reshape(-1)
            animSteps = animSteps[animSteps != 0]
            nA = len(animSteps)
            if nA <= nSteps: #or nA <= bins:
                if nA < nSteps:
                    nSteps = nA
                    print("Using %d steps"%nSteps)
                groupData[t,i,:nSteps] = animSteps[:nSteps]
            else:

#                groupData[t,i,:nSteps] = densitySample(animSteps,nSteps,bins) 
                groupData[t,i,:nSteps] = animSteps[:nSteps] 
#                groupData[t,i,:nSteps] = tailSamples(animSteps,nSteps)
#                groupData[t,i,:nSteps] = animSteps[np.random.permutation(len(animSteps))][:nSteps]
                
    return groupData
