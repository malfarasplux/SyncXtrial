#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:13:38 2019

@author: shadi
"""

# Module Syncmetrics

# Program to implement sync assessment measurements between resp signals
# https://www.biosignalsplux.com/notebooks/Categories/Load/open_h5_rev.php
from h5py import File
import numpy as np
import biosignalsnotebooks as bsnb # biosignalsnotebooks
from scipy.signal import hilbert 
from scipy.stats import linregress
from scipy.signal import coherence

from sklearn import preprocessing 
from sklearn.metrics.pairwise import cosine_similarity
import novainstrumentation as ni

from neurokit import rsp_process


#                   normalized_amplitude,  #amplitude #miq
#                   sign_diff,             #time #miq
#                   cosine_similarity]     #amplitude #miq


######### MIQUEL #############################################################
##############################################################################

# Import data
def loadsignal(fname,channel,txtfile=False):
    if txtfile:
        file = fname + ".txt"
        txtdata = np.loadtxt(file)
        data = txtdata[:,channel+1].reshape(-1,1)
        srate = 1000
        rawtime = (np.arange(len(data))/srate).reshape(-1,1)
        print("txtload")
    else:
        channel = "channel_" + str(channel)
        fname = fname + ".h5"
        h5_object = File(fname)
        h5_group = h5_object.get('00:07:80:58:9B:3F')
        srate = h5_group.attrs.get("sampling rate")
        h5_sub_group = h5_group.get("raw")
        data_chan = h5_sub_group.get(channel)
        data = [item for sublist in data_chan for item in sublist]
        rawtime = np.array(bsnb.generate_time(data, srate))
        rawtime = rawtime.reshape(-1,1)
    return (np.array(data, dtype=np.float64)).reshape(-1,1), rawtime, srate

# Signal clipping (slice)
def signalclipping():
    #TODO
    pass
    return True


# ni 100 Smoothing (with reshape safeguard)
def smoothing(a):
    """novainstrumentation 100 smoothing
    Reshape safeguard used to work with column arrays
    TODO: Check causality
    """
    is_reshaped = False
    if a.ndim != 1:
        shape = a.shape
        if shape[1] == 1:
            a = a.reshape(len(a))
            is_reshaped = True
    return ni.smooth(a.reshape(len(a)),100).reshape(-1,1)

#smooth_A = ni.smooth(signal_A,100)
#smooth_B = ni.smooth(signal_B,100)
#smooth_A = ni.smooth(signal_A.reshape(len(signal_A)),100)
#smooth_B = ni.smooth(signal_B.reshape(len(signal_B)),100)
##smooth_A = smoothing(signal_A)
##smooth_B = smoothing(signal_B)

# Midpoint


# Normalisation
##norm_A = (preprocessing.normalize(signal_A, norm='max', axis=0))
##norm_B = (preprocessing.normalize(signal_B, norm='max', axis=0))

# Signal difference
def sigdiff(a, b):
    """Return signal difference """
    return (b - a)

def normalise(a):
    """Maxmin normalise """
    return (preprocessing.normalize(a, norm='max', axis=0))

def normdiff(a, b):
    """Maxmin normalise and return mean difference
    Only relevant for postprocessing or long windows
    """
    norm_A = (preprocessing.normalize(a, norm='max', axis=0))
    norm_B = (preprocessing.normalize(b, norm='max', axis=0))
    return np.mean(norm_B - norm_A)

# Similar derivative
def similar_der(a, b):
    """Similar derivative coefficient
    Computes how similarly two signals evolve together taking the derivative sign
    Only relevant when derivatives are taken form smooth signals
    signal length must be > 1 
    """
    der_a = np.diff(a, axis = 0)
    der_b = np.diff(b, axis = 0)
    equalsign = ((der_a > 0) == (der_b > 0))
    return np.sum(equalsign)/len(equalsign)

# Similar derivative smooth
def similar_der_smooth(a, b):
    """Similar derivative smooth coefficient
    Computes how similarly two signals evolve together taking the derivative sign
    Taken form smoothed signals
    signal length must be > 1 
    """
    der_a = np.diff(smoothing(a), axis = 0)
    der_b = np.diff(smoothing(b), axis = 0)
    equalsign = ((der_a > 0) == (der_b > 0))
    return np.sum(equalsign)/len(equalsign)

# Relative integral
def relative_int(a, b):
    """Similar relative integral coefficient sum(b)/sum(a)
    1 --> similarity
    Above and below
    """
    return np.sum(b) / np.sum(a) # Relative b/a version

# Average differences (reference integral)
def avg_difference(a, b):
    """Average difference (reference integral)
    0 --> similarity
    """
    return (np.mean(b) - np.mean(a)) # Reference around [0] version

# Cosine similarity
def cos_similarity(a, b):
    """Cosine similarity between 2 vectors """
    return (cosine_similarity(a.reshape(1,-1),b.reshape(1,-1))) 

# Compute metric slw
def compute_metric_slw(a,b,f, window=1000, overlap=.5):
    """Compute metric over a sliding window 
    window is expressed in samples
    overlap sets the steps for the sliding window
    returns averaged result value in window and times at computation 
    """
    result = []
    time = []
    time_x = []
    win = window
    
    s = len(a)
    # dim = int((s-win)/(win*(1-overlap))) 
    dim = int((s-win)/(win*(1-overlap))) + 1 
    print (s)  
    print (dim)
    for i in range(dim):        
        i_s = int(i*win*(1-overlap))
        wa = a[i_s: i_s + win]
        wb = b[i_s: i_s + win]
        time += [i_s]
        time_x += [i_s + win]
        result += [f(wa,wb)]
#    return (np.array(result)), (np.array(time)) 
    return (np.array(result)).reshape(-1,1), (np.array(time_x)).reshape(-1,1)

##### SHADI ###################################################################
##############################################################################

# Linear regression corr coeffcient
def lin_reg_r_metric(a,b):
    # 1 dim step added
    if a.ndim != 1:
        a = a.reshape(len(a))
    if b.ndim != 1:
        b = b.reshape(len(b))
    return linregress(a,b)[2]

# Corr coefficient
# Problems/warnings 1d scipy
def correlation_coeff(a,b):
    corr_mat=np.corrcoef(a,b)
    corr_coef=corr_mat[0,1]
    return corr_coef

# Instantaneous phase
# TODO hardcoded srate problem
def comp_inst_phase(x_temp):
    if x_temp.ndim != 1:
        x_temp = x_temp.reshape(len(x_temp))
    sampling_rate = 1000
    analytic_signal = hilbert(x_temp)
    analytic_signal=np.array(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) /(2.0*np.pi) * sampling_rate)
    instantaneous_frequency = np.append(instantaneous_frequency,instantaneous_frequency[-1])
    return instantaneous_frequency

## phase difference## 
# TODO: Check order convention b,a
def inst_phase_difference(a,b):  
    inst_phase_sig1=comp_inst_phase(a)
    inst_phase_sig2=comp_inst_phase(b) 
    phase_diff=np.mean(inst_phase_sig1-inst_phase_sig2)
    return phase_diff

## mean phase coherence
# TODO: Check order convention b,a
def MPC(a,b):
    inst_phase_sig1=comp_inst_phase(a)
    inst_phase_sig2=comp_inst_phase(b)
    inst_phase_diff=inst_phase_sig1-inst_phase_sig2
    mpc = (np.mean(np.cos(inst_phase_diff))**2 + np.mean(np.sin(inst_phase_diff))**2)**(0.5);
    return mpc 

# signal coherence ?
# why is nperseg = 1024 ? 
# TODO Check reference https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.coherence.html
# TODO Hardcoded sampling rate problem
def MSC(a,b):
#    f, Cxy = coherence(a, b , sampling_rate, nperseg=1024)if a.ndim != 1:
    if a.ndim != 1:
        a = a.reshape(len(a))
    if b.ndim != 1:
        b = b.reshape(len(b))
    
    sampling_rate = 1000
    f, Cxy = coherence(a, b , sampling_rate)
    coh_mean=np.mean(Cxy)
    return coh_mean

# whitening (mean, std normalisation)
def wh(s):
    """whitening"""
    return (s-np.mean(s))/np.std(s)



# SHADI's neurokit peak detection 
def rsp_peak_detect(a, sampling_rate, th_scale):
    onset = rsp_process(a.reshape(len(a)),sampling_rate)["RSP"]["Expiration_Onsets"]
    th = th_scale * np.mean(a)
    ind_cycle = []
    
    # Remove below threshold th
    for i in range(len(onset)):
        amp_peak = a[onset[i]]
        if amp_peak > th:
            ind_cycle += [onset[i]]
    return ind_cycle


