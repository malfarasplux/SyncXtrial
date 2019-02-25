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

text_list_of_metrics = [ "similar der_smooth",    # similar derivative sm
                         "similar der",           # similar derivative
                         "relative_int",          # relative area B/A (integral)
#                         "cosine_similarity",     # cosine similarity CRASH                        
#                         "correlation_coeff",    # correlation coefficient 
                         "normdiff",              # normalised diff
                         "lin_reg_r"]             # linear regression correl
                           

list_of_metrics_slw = [syncm.similar_der_smooth,
                      syncm.similar_der,
                      syncm.relative_int,
#                      syncm.cos_similarity,
#                      syncm.correlation_coeff,
                      syncm.normdiff,
                      syncm.lin_reg_r_metric]



# Compute and plot in a loop
fig, axs = plt.subplots(len(text_list_of_metrics),1, figsize=(15, 6), facecolor='w', edgecolor='k')
i = 0
for metric in list_of_metrics_slw:
    m,t = syncm.compute_metric_slw(signal_A,signal_B,metric, window=10000,overlap=.95)  ## window=win , half win, double win
    axs[i].plot(t,m, label=text_list_of_metrics[i])
    title = text_list_of_metrics[i]
    axs[i].set_title(title)
    i=i+1


#f, axs = plt.subplots(2, 2)
#axarr[0].set_title('Axis [0]')

# Labels
#for ax in axs.flat:
#    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right plots.
#for ax in axs.flat:
#    ax.label_outer()
    
    
    
M, T = syncm.compute_metric_slw(signal_A,signal_B,syncm.lin_reg_r_metric, window=10000,overlap=.95)
M, T = syncm.compute_metric_slw(signal_A.reshape(len(signal_A)),signal_B.reshape(len(signal_B)),syncm.lin_reg_r_metric, window=10000,overlap=.95)