# Program to implement sync assessment measurements between biosignals
# https://www.biosignalsplux.com/notebooks/Categories/Load/open_h5_rev.php
from h5py import File
import numpy as np
import matplotlib.pyplot as plt
import biosignalsnotebooks as bsnb # biosignalsnotebooks

# Import
file_path = "D:\Dropbox\PLUX_docs\Shadi_2019\Acquisitions\opensignals_000780589B3F_2019-02-13_17-03-44.h5"
h5_object = File(file_path)

# Key list (.h5 hierarchy ground level)
list(h5_object.keys())

# Access to the second hierarchy level through group key "mac" 
h5_group = h5_object.get('00:07:80:58:9B:3F')
print ("Second hierarchy level: " + str(list(h5_group)))

# h5_group metadata attributes 
print ("Metadata of h5_group: \n" + str(list(h5_group.attrs.keys())))

# Storage of acquisition sampling rate by accessing h5_group metadata (attributes) 
sampling_rate = h5_group.attrs.get("sampling rate")
print ("Sampling Rate: " + str(sampling_rate))

# third level of data through group key "mac" and sub-group key "raw" 
h5_sub_group = h5_group.get("raw")
print("Third hierarchy level: " + str(list(h5_sub_group)))

data_chan1 = h5_sub_group.get("channel_1")
data_A = [item for sublist in data_chan1 for item in sublist]
data_chan2 = h5_sub_group.get("channel_2")
data_B = [item for sublist in data_chan2 for item in sublist]

signal_A = np.array(data_A, dtype=np.int64)
signal_B = np.array(data_B, dtype=np.int64)

time = np.array(bsnb.generate_time(data_A, sampling_rate))

# Signal data representation.

plt.show()
plt.plot(time, data_A)
plt.plot(time, data_B)

# Function to subtract 2 signals. Signals can be optionally sliced
def subtract(sigA, sigB, minX=None, maxX=None):
    # TODO
    # Check for signal lenght conflicts
    
    if maxX < minX:
        print("ERROR")
    
    else:
        if maxX != None:
            sigA = sigA[:maxX]
            sigB = sigB[:maxX]
        if minX != None:
            sigA = sigA[minX:]
            sigB = sigB[minX:]
                
    return sigB-sigA


signal_C = subtract(signal_A, signal_B, 10,20)
     



