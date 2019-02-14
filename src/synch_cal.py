from numpy import array
from h5py import File
import matplotlib.pyplot as plt
import biosignalsnotebooks as bsnb
#import scipy.signal 
from scipy.signal import hilbert 
import numpy as np 



###### load data #####
# signal 1 path
file_path1 = "opensignals_000780589B3F_2019-02-13_17-03-44.h5"

# file 1
h5_object1 = File(file_path1)
list(h5_object1.keys())


h5_group1 = h5_object1.get('00:07:80:58:9B:3F')
#print ("Second hierarchy level: " + str(list(h5_group)))
#print ("Metadata of h5_group: \n" + str(list(h5_group.attrs.keys())))
sampling_rate1 = h5_group1.attrs.get("sampling rate")
#print ("Sampling Rate: " + str(sampling_rate))
h5_sub_group1 = h5_group1.get("raw")
print("Third hierarchy level: " + str(list(h5_sub_group1)))
h5_data1 = h5_sub_group1.get("channel_1")
h5_data2 = h5_sub_group1.get("channel_2")


# Conversion of a nested list to a flatten list by list-comprehension
# The following line is equivalent to:
# for sublist in h5_data:
#    for item in sublist:
#        flat_list.append(item)
data_list1 = [item for sublist in h5_data1 for item in sublist]
time1 = bsnb.generate_time(data_list1, sampling_rate1)

data_list2 = [item for sublist in h5_data2 for item in sublist]
##### sychorny indices ##### 





# Signal data samples values and graphical representation.
print (array([item for sublist in h5_data1 for item in sublist]))
plt.plot(time1,data_list1)

plt.plot(time1,data_list2)




### respirstion signal pre-processing ### 

## windowing#
fs=100
start=0*fs
fin =5*fs
overlap=1*fs





## instantanous phase ## 
def comp_inst_phase(x_temp):
    fs = 100    #carefull! sampling frequency is hard coded here...
    analytic_signal = hilbert(x_temp)
    analytic_signal=np.array(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) /(2.0*np.pi) * fs)
    instantaneous_frequency = np.append(instantaneous_frequency,instantaneous_frequency[-1])
    return instantaneous_frequency

analytic_signal1=np.array(data_list1)
inst_phase_sig1=comp_inst_phase(analytic_signal1)

analytic_signal2=np.array(data_list2)
inst_phase_sig2=comp_inst_phase(analytic_signal2)
phase_sync=inst_phase_sig1-inst_phase_sig2
plt.figure()
plt.plot(time1,phase_sync)





## correlation ## 
  #scipy.signal.correlate(in1, in2, mode='full', method='auto')
  
#winCount = 0;
#while fin <= len(data_list1):
#    winval = data_list1[start:fin];
#    winCount = winCount + 1;
#        ## apply inst_phase## 
#    analytic_signal = hilbert(winval)   
#    analytic_signal1=np.array(analytic_signal)
#    instantaneous_phase = np.unwrap(np.angle(analytic_signal1))
#    instantaneous_frequency = (np.diff(instantaneous_phase) /(2.0*np.pi) * fs)
#    instantaneous_frequency = np.append(instantaneous_frequency,instantaneous_frequency[-1])    
#        
#        
#        
#        
#    inst_phase_all.append(instantaneous_frequency)
#    start = start + overlap;
#    fin = fin + overlap;
    

## plot the inst_phase_freq