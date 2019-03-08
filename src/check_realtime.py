# Shadi's code to check real-time match with offline plotting
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 13:55:49 2019

@author: shadi
"""

# Main sync eval
#import os
#import sys
#file_dir = os.path.dirname("/Users/shadi/PycharmProjects/GitHub_code/SyncXtrial/src/syncmetric_bitalino.py")
#sys.path.append(file_dir)
import syncmetrics_bitalino as syncm
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing 
import novainstrumentation as ni

#Load signals
txtload = True
#filepath = "./BVP_RESPchest_4_1_4"
## file path 
file_folder = "/Users/shadi/PycharmProjects/GitHub_code/SyncXtrial/src"

#file_folder = "/Users/shadi/PycharmProjects/GitHub_code/SyncXtrial/resp_acuqi_bitalino/kat_rui"
#file_name = "kat_rui_3-2-3-2"
file_name = "realtime"

#file_name = "kat_rui_3-3-4-4"
 #file_name = "BVP_RESPchest_3_2_3_4_1_4.h5"

filepath= file_folder + "/" + file_name
## bitalino
#raw_A, rawtime, srate = syncm.loadsignal(filepath, 4, txtload)
#raw_B, rawtime, srate = syncm.loadsignal(filepath, 5, txtload)
## biosignalsplux
raw_A, rawtime, srate = syncm.loadsignal(filepath, 1, txtload)
raw_B, rawtime, srate = syncm.loadsignal(filepath, 2, txtload)
## free variables 
## for kat_rui_3-2-3-2"
#th_scale_A=1.2
#th_scale_B=1.2
th_scale_A=1.2
th_scale_B=1.2


window_size=15000
overlap=0.99
#Signal  clipping
startpoint = 0
endpoint = -1
#startpoint = 0
#endpoint = -1
#startpoint = 0
#endpoint = len(raw_A)
signal_A = raw_A[startpoint:endpoint]
signal_B = raw_B[startpoint:endpoint]
time = rawtime[startpoint:endpoint]
t_offset = time[0]
time = time - t_offset
sampletime = np.arange(len(signal_A))

# SHADI's neurokit RSP peak detect
#detect_peaks = True
#if detect_peaks:
#    rsp_onset_A = syncm.rsp_peak_detect(signal_A, srate,th_scale_A)
#    rsp_onset_B = syncm.rsp_peak_detect(signal_B, srate,th_scale_B)
##    plt.plot(time, signal_A, '-gD', markevery=rsp_onset_A, marker='o', color='b')
##    plt.plot(time, signal_B, '-gD', markevery=rsp_onset_B, marker='o', color='g')
#    rsp_time_A = np.diff(np.array(rsp_onset_A), axis=0)
#    rsp_time_B = np.diff(np.array(rsp_onset_B), axis=0)
    



text_list_of_metrics = [ "lin_reg_r",
                         "inst_phase_difference",
                         "MPC",
                         "MSC",
                         "similar der_smooth",    # similar derivative sm
                         "similar der",           # similar derivative
                         "relative_int",          # relative area B/A (integral)
                         "normdiff",              # normalised diff
                         "cosine_similarity"]     # cosine similarity (reshape needed) CRASH                        
#                         "correlation_coeff",    # correlation coefficient 
#                         "lin_reg_r"]             # linear regression correl
                           

list_of_metrics_slw = [syncm.lin_reg_r_metric,
                      syncm.inst_phase_difference,
                      syncm.MPC,
                      syncm.MSC,
                      syncm.similar_der_smooth,
                      syncm.similar_der,
                      syncm.relative_int,
                      syncm.normdiff,
                      syncm.cos_similarity
#                      syncm.correlation_coeff,
#                      syncm.lin_reg_r_metric
                      ]




###############################################################################
# Plot
def get_delay(a,b,onset_a,onset_b):
    zaman=[]
    min_len=np.min([len(onset_a),len(onset_b)])
    if  np.size(onset_a) > min_len:
        onset_a=onset_a[0:min_len]
    if  np.size(onset_b)>min_len:
        onset_b=onset_b[0:min_len]
          
    delay=abs(np.array(onset_a)-np.array(onset_b))
    amp_peak_a=a[np.array(onset_a)];
    amp_peak_b=b[np.array(onset_b)];
    peak_diff=abs(np.array(amp_peak_a)-np.array(amp_peak_b))
    
    for i in range(min_len):
        sign=np.array(onset_a[i])-np.array(onset_b[i])
        if sign>0:
            zaman +=[onset_a[i]]
        else:
            zaman +=[onset_b[i]]
    return zaman, delay, peak_diff

#onset_a=rsp_onset_A
#onset_b=rsp_onset_B
#a=signal_A
#b=signal_B



#Z, D, PD = get_delay(signal_A, signal_B, rsp_onset_A, rsp_onset_B)


fig, axs = plt.subplots(6,2, facecolor='w', edgecolor='k')

axs[0,0].plot(time,signal_A)
axs[0,0].plot(time,signal_B)
axs[0,0].set_title('Peak detection in signals')

#axs[1,0].stem(Z,D) 
#axs[1,0].set_title('Time Delay of peaks')
#axs[2,0].stem(Z,PD)
#axs[2,0].set_title('Amp Delay of peaks')


i=0
i_offset = 3
plotdim = 6
#j = 2
#for metric in list_of_metrics_slw[:j]:
#M=[]
for metric in list_of_metrics_slw:
    print(metric)
    m,t = syncm.compute_metric_slw(signal_A,signal_B,metric,window_size,overlap)  ## window=win , half win, double win
   # M[i] = m 
#    axs[i + i_offset].plot(t,m)
#    axs[int((i + i_offset) % plotdim),int((i + i_offset)/plotdim)].plot(t, m, str('C' + str((i+1))),label=text_list_of_metrics[i])

    axs[int((i + i_offset) % plotdim),int((i + i_offset)/plotdim)].plot(t, m, str('C' + str((i+1))))
    axs[int((i + i_offset) % plotdim),int((i + i_offset)/plotdim)].set_title(text_list_of_metrics[i])
    i=i+1
#m,t = syncm.compute_metric_slw(signal_A,signal_B,"MPC")  ## window=win , half win, double win
