# Main sync eval
import syncmetrics as syncm
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing 
import novainstrumentation as ni

#Load signals
raw_A, rawtime, srate = syncm.loadsignal(".\BVP_RESPchest_4_1_4.h5", "channel_1")
raw_B, rawtime, srate = syncm.loadsignal(".\BVP_RESPchest_4_1_4.h5", "channel_3")

#Signal  clipping
#startpoint = 70*srate
#endpoint = -10*srate
startpoint = 0
endpoint = len(raw_A)
signal_A = raw_A[startpoint:endpoint]
signal_B = raw_B[startpoint:endpoint]
time = rawtime[startpoint:endpoint]
sampletime = np.arange(len(signal_A))

# SHADI's neurokit RSP peak detect
detect_peaks = False
if detect_peaks:
    rsp_onset_A = syncm.rsp_peak_detect(signal_A, srate)
    rsp_onset_B = syncm.rsp_peak_detect(signal_B, srate)
    plt.plot(time, signal_A, '-gD', markevery=rsp_onset_A, marker='o', color='b')
    plt.plot(time, signal_B, '-gD', markevery=rsp_onset_B, marker='o', color='g')
    rsp_time_A = np.diff(np.array(rsp_onset_A), axis=0)
    rsp_time_B = np.diff(np.array(rsp_onset_B), axis=0)
    



text_list_of_metrics = [ "similar der_smooth",    # similar derivative sm
                         "similar der",           # similar derivative
                         "relative_int",          # relative area B/A (integral)
                         "normdiff",              # normalised diff
                         "cosine_similarity",     # cosine similarity (reshape needed) CRASH                        
#                         "correlation_coeff",    # correlation coefficient 
                         "lin_reg_r"]             # linear regression correl
                           

list_of_metrics_slw = [syncm.similar_der_smooth,
                      syncm.similar_der,
                      syncm.relative_int,
                      syncm.normdiff,
                      syncm.cos_similarity,
#                      syncm.correlation_coeff,
                      syncm.lin_reg_r_metric]



# Compute and PLOT in a loop
fig, axs = plt.subplots(len(text_list_of_metrics),1, figsize=(15, 9), facecolor='w', edgecolor='k')
i = 0
for metric in list_of_metrics_slw:
    m,t = syncm.compute_metric_slw(signal_A,signal_B,metric, window=10000,overlap=.95)  ## window=win , half win, double win
#    m,t = syncm.compute_metric_slw(signal_B,signal_B,metric, window=10000,overlap=.95)  ## window=win , half win, double win
#    m,t = syncm.compute_metric_slw(signal_B,signal_B,metric, window=10000,overlap=.95)  ## window=win , half win, double win
#    m,t = syncm.compute_metric_slw(syncm.normalise(signal_B),syncm.normalise(signal_A),metric, window=10000,overlap=.95)  ## window=win , half win, double win
    axs[i].plot(t, m,  str('C' + str((i+1))),label=text_list_of_metrics[i])
    title = text_list_of_metrics[i]
    axs[i].set_title(title)
    i=i+1

