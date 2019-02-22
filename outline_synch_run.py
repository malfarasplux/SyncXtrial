#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:05:13 2019

@author: shadi
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 16:01:12 2019

@author: hgamboa
"""


from pylab import *

from scipy.stats import linregress
from numpy import array
from h5py import File
import matplotlib.pyplot as plt
import biosignalsnotebooks as bsnb
#import scipy.signal 
from scipy.signal import hilbert 
from scipy import signal
#import mlpy
import numpy as np 
import matplotlib.cm as cm
import neurokit as nk
import novainstrumentation as ni


## load data with text##

#file = "BVP_RESPchest_3_2_3.txt"

#file = "BVP_RESPchest_4_1_4.txt"

#l = loadtxt(file)


###### load data #####
# signal 1 path
file_folder = "/Users/shadi/PycharmProjects/plux_internship"
file_name = "BVP_RESPchest_3_2_3.h5"
#file_name = "BVP_RESPchest_4_1_4.h5"
#file_name = "BVP_RESPchest_3_2_3_4_1_4.h5"

file_path1 = file_folder + "/" + file_name

#file_path1 = "BVP_RESPchest_4_1_4.h5"

# file 1
h5_object1 = File(file_path1)
list(h5_object1.keys())


h5_group1 = h5_object1.get('00:07:80:58:9B:3F')
#print ("Second hierarchy level: " + str(list(h5_group)))
#print ("Metadata of h5_group: \n" + str(list(h5_group.attrs.keys())))
sampling_rate = h5_group1.attrs.get("sampling rate")
#print ("Sampling Rate: " + str(sampling_rate))
h5_sub_group1 = h5_group1.get("raw")
print("Third hierarchy level: " + str(list(h5_sub_group1)))
h5_data1 = h5_sub_group1.get("channel_1")
h5_data2 = h5_sub_group1.get("channel_3")
data_list1 = [item for sublist in h5_data1 for item in sublist]
miquel=data_list1[70*sampling_rate:len(data_list1)-10*sampling_rate]
miquel_np=np.array(miquel)

data_list2 = [item for sublist in h5_data2 for item in sublist]
shadi=data_list2[70*sampling_rate:len(data_list2)-10*sampling_rate]
shadi_np=np.array(shadi)
time1 = bsnb.generate_time(data_list1, sampling_rate)
time=time1[70*sampling_rate:len(data_list1)-10*sampling_rate]
time=time-time[0]
time_arr=np.array(time)

def wh(s):
    "whitening"
    return (s-mean(s))/std(s)




## windowing## 
#a=miquel
#b=shadi

def comp_inst_phase(x_temp):
    sampling_rate=1000
    analytic_signal = hilbert(x_temp)
    analytic_signal=np.array(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) /(2.0*np.pi) * sampling_rate)
    instantaneous_frequency = np.append(instantaneous_frequency,instantaneous_frequency[-1])
    return instantaneous_frequency

 
def compute_metric_slw(a,b,f, window, overlap):

    result = []
    time = []
    win = window
    
    s = len(a)
    print (s)
    for i in range(int((s-win)/(win*(1-overlap)))):        
        i_s = int(i*win*(1-overlap))
        wa = a[i_s: i_s + win]
        wb = b[i_s: i_s + win]
        time += [i_s]
        result += [f(wa,wb)]
        
        #plot(wa,wb)

    return array(result), array(time) 

####### in case we want cycle analysis### (the problem of not having cycles with the same length for signals)
#def compute_metric_cycle(a,b,f):
#
#    result = []
#    time = []
#   ## peak detection## 
#   
#    # peak detection 
#    processed_a = nk.rsp_process(a,sampling_rate=1000)
#    df_a=processed_a["RSP"]
#    onset_a=df_a["Expiration_Onsets"]
#    
#    processed_b = nk.rsp_process(b,sampling_rate=1000)
#    df_b=processed_b["RSP"]
#    onset_b=df_b["Expiration_Onsets"]
#    
#    ##peak correction## 
#    
#    ind_cycle_a=onset_a     ## sample number of the peak
#    ind_cycle_b=onset_b     ## sample number of the peak
#
#  
#    for i in range(min(len(ind_cycle_a),len(ind_cycle_b))-10):        
#        wa = a[ind_cycle_a[i]:ind_cycle_a[i+1]]
#        wb = b[ind_cycle_b[i]:ind_cycle_b[i+1]]
#        time += max(ind_cycle_a[i+1],ind_cycle_b[i+1])
#        result += [f(wa,wb)]
#        
#        #plot(wa,wb)
#
#    return array(result), array(time) 

#def compute_metric_cycle(a,b):

   ## peak detection## 
   
    # peak detection 
processed_a = nk.rsp_process(miquel,sampling_rate=1000)
df_a=processed_a["RSP"]
onset_a=df_a["Expiration_Onsets"]
    
processed_b = nk.rsp_process(shadi,sampling_rate=1000)
df_b=processed_b["RSP"]
onset_b=df_b["Expiration_Onsets"]
#plt.plot(time,miquel,'-gD',markevery=onset_a,marker='o', color='b')
#plt.plot(time,shadi,'-gD',markevery=onset_b,marker='o', color='g')
    ##peak correction##
# for 4_1_4    
#th1=np.mean(miquel_np)+np.mean(miquel_np)*0.6
#th2=np.mean(shadi_np)+np.mean(shadi_np)*0.6
# for 3_2_3 , 4_1_4    
th1=np.mean(miquel_np)
th2=np.mean(shadi_np)+np.mean(shadi_np)*0.3
# for 3_2_3    
th1=np.mean(miquel_np)
th2=np.mean(shadi_np)+np.mean(shadi_np)*0.6


ind_cycle_a=[]
for i in range(len(onset_a)):
    amp_peak1=miquel[onset_a[i]]
    if amp_peak1>th1:
        ind_cycle_a+=[onset_a[i]]

ind_cycle_b=[]

for i in range(len(onset_b)):
    amp_peak2=shadi[onset_b[i]]
    if amp_peak2>th2:
        ind_cycle_b+=[onset_b[i]]
        

plt.plot(time,miquel,'-gD',markevery=ind_cycle_a,marker='o', color='b')
plt.plot(time,shadi,'-gD',markevery=  ind_cycle_b,marker='o', color='g')
        
    
    #return ind_cycle_a,ind_cycle_b

  

#def peak_delay(ind_cycle_a,ind_cycle_b):
zaman=[]
min_len=min(len(ind_cycle_a),len(ind_cycle_b))
if  size(ind_cycle_a)>min_len:
    ind_cycle_a=ind_cycle_a[0:min_len]
if  size(ind_cycle_b)>min_len:
    ind_cycle_b=ind_cycle_b[0:min_len]
      
delay=abs(np.array(ind_cycle_a)-np.array(ind_cycle_b))
amp_peak_a=miquel_np[np.array(ind_cycle_a)];
amp_peak_b=shadi_np[np.array(ind_cycle_b)];
peak_diff=abs(np.array(amp_peak_a)-np.array(amp_peak_b))

for i in range(min_len):
    sign=np.array(ind_cycle_a[i])-np.array(ind_cycle_b[i])
    if sign>0:
        zaman +=[ind_cycle_a[i]]
    else:
        zaman +=[ind_cycle_b[i]]
# peak_amplitude

           
   #return delay,zaman
#plt.figure()      
#plt.stem(zaman,delay)   



## matrices with only sliding window   

    
def lin_reg_r_metric(wa,wb):
    return linregress(wa,wb)[2]
def inst_phase_difference(wa,wb):  
    inst_phase_sig1=comp_inst_phase(wa)
    inst_phase_sig2=comp_inst_phase(wb) 
    phase_diff=np.mean(inst_phase_sig1-inst_phase_sig2)
    return phase_diff

def MPC(wa,wb):
    inst_phase_sig1=comp_inst_phase(wa)
    inst_phase_sig2=comp_inst_phase(wb)
    inst_phase_diff=inst_phase_sig1-inst_phase_sig2
    mpc = (np.mean(np.cos(inst_phase_diff))**2 + np.mean(np.sin(inst_phase_diff))**2)**(0.5);
    return mpc 



def MSC(wa,wb):
    f, Cxy = signal.coherence(wa, wb , sampling_rate, nperseg=1024)
    coh_mean=np.mean(Cxy)
    return coh_mean




    
#plt.figure()
#plt.semilogy(f, Cxy)
#plt.xlabel('frequency [Hz]')
#plt.ylabel('Coherence')
#plt.show()   

def correlation_coeff(wa,wb):
    corr_mat=np.corrcoef(wa,wb)
    corr_coef=corr_mat[0,1]
    return corr_coef


### metrics with cycles 
#def peak_delay(wa,wb):
#    
#
### metrics instans
#def inst_phase_difference:



### sliding window## 
 
#list_of_metrics = [lin_reg_r_metric,      # amplitude #hugo
#                   peak_delay,            # event, time  #sh done
#                   inst_phase_difference, # spectral  #sh done
#                   cross_correlation_lag, # time   #sh     time lag correlation 
#                   cross_correlation_max, # amplitude #sh
#                   correlation_coeff,     # amplitude #sh done 
#                   sign_diff,             #time #miq
#                   normalized_amplitude,  #amplitude #miq
#                   peak_amplitude,        #time, amplitude #sh
#                   MSC,             # spectral #sh done
#                   mean_phase_coherence,  # spectral #sh done 
#                   dtw,                   #time #sh..
#                   cosine_similarity]     #amplitude #miquel
#
#text_list_of_metrics = [ "lin_reg_r_metric",      # amplitude
#                         "peak_delay",            # event, time
#                         "inst_phase_difference", # spectral 
#                         "cross_correlation_lag", # time
#                         "cross_correlation_max", # amplitude
#                         "correlation_coeff",     # amplitude #sh
#                         "sign_diff",             #time
#                         "normalized_amplitude",  #amplitude 
#                         "peak_amplitude",        #time, amplitude 
#                         "MSC",             # spectral
#                         "mean_phase_coherence",  # spectral
#                         "dtw",                   #time
#                         "cosine_similarity"]     #ampl 


#list_of_metrics_slw = [lin_reg_r_metric,      # amplitude #hugo
#                   inst_phase_difference,
#                   cross_correlation_lag, # time   #sh
#                   cross_correlation_max, # amplitude #sh
#                   sign_diff,             #time #miq
#                   correlation_coeff,
#                   normalized_amplitude,  #amplitude #miq
#                   coherence,             # spectral #sh
#                   mean_phase_coherence,  # spectral #sh
#                   dtw,                   #time #sh..
#                   cosine_similarity]     #amplitude #miquel
list_of_metrics_slw = [correlation_coeff,
                     inst_phase_difference,
                     MPC,
                     MSC]
text_list_of__metrics_slw = ['correlation_coeff',
                     'inst_phase_difference',
                     'MPC',
                     'MSC']
                       
                       
                      
                         # amplitude #hugo
        
#
#list_of_metrics_cycle = [lin_reg_r_metric,      # amplitude #hugo
#                   peak_delay,            # event, time  #sh
#                   inst_phase_difference, # spectral  #sh
#                   cross_correlation_lag, # time   #sh
#                   cross_correlation_max, # amplitude #sh
#                   sign_diff,             #time #miq
#                   normalized_amplitude,  #amplitude #miq
#                   peak_amplitude,        #time, amplitude #sh
#                   coherence,             # spectral #sh
#                   mean_phase_coherence,  # spectral #sh
#                   dtw,                   #time #sh..
#                   cosine_similarity]     #amplitude #miquel


#fig, axs = plt.subplots(7,1, figsize=(15, 6), facecolor='w', edgecolor='k')
fig, axs = plt.subplots(7,1, facecolor='w', edgecolor='k')

axs[0].plot(time,miquel,'-gD',markevery=ind_cycle_a,marker='o', color='b')
axs[0].plot(time,shadi,'-gD',markevery=  ind_cycle_b,marker='o', color='g')
axs[0].set_title('Peak detection in signals')

axs[1].stem(zaman,delay) 
axs[1].set_title('Time Delay of peaks')
axs[2].stem(zaman,peak_diff)
axs[2].set_title('Amp Delay of peaks')

# time delay plots

#fig=plt.figure(figsize=(2, 2),facecolor='w', edgecolor='k')
i=3
j=0
for metric in list_of_metrics_slw:
    
    m,t = compute_metric_slw(miquel,shadi,metric, window=12000,overlap=.9)  ## window=win , half win, double win
    axs[i].plot(t,m)
    axs[i].set_title(text_list_of__metrics_slw[j])
    #fig[i].ylabel(metric)

    #plt.xlabel('frequency [Hz]')
#plt.ylabel('Coherence')
    i=i+1
    j=j+1

   


        
#
#for metric_cycle in list_of_metrics_cycle:
#    
#    m_cycle,t_cycle = compute_metric_cycle(a,b,metric)
    ## store all the outputs  # miq
    

    
                       
#### plots in loop## 
#
#subplot(2,1,1)
#title(file)
#ylabel("r error")
#ylim(-1,1)
#plot(t,m)
#
#subplot(2,1,2)
#plot(wh(a))
#plot(wh(b)+3)
#
#show()
