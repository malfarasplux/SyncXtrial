# SyncXtrial
Synchrony exploration through a sensing lens (PLUX sensors + OpenSignals + python)

[0. Todo list(20190228)](#todo)  
[1. Tools required](#prereq)  
[2. Sensing platform documentation](#docs)  
[3. Extra resources](#resrc)  
[4. Configuration](#config)  

##  Code to assess synchrony between two signals <a name="syncassess"></a>
[syncmetrics.py](./src/sync_assess.py)  
[get_sync.py](./src/sync_assess.py)  

##  0. TODO List<a name="todo"></a>
- Fix peak detection (and check with other signals)  
- New acquisitions with BITalino + Breathe app (make sure the sensor doesn't saturate)  
- Check Channels 1,2,3,4
- Prepare report (3000, 6000, 15000)
- Smooth the signal 
- Look in detail the region where plots show synchrony. What happens?  
- ServerBIT OSC calls after processing buffer / Or MIDI protocol instead
- Dynamical plots in python https://github.com/pyqtgraph/pyqtgraph/tree/develop/examples  
- Obtain feature vectors (saved as .txt) for audio mapping 
- Defining the sync level from the integration of features  
- New thread for plotting  


##  1. Tools required <a name="prereq"></a>
- PLUX sensing platform + 2xPZT respiration sensors  
https://bitalino.com/  
https://www.biosignalsplux.com/en/explorer

- Pyhton (v > 3.5)  
https://www.python.org/downloads/

- PLUX OpenSignals (r)evolution Software  
https://www.biosignalsplux.com/en/software  

- (Recommended) Anaconda + Python  
 https://www.anaconda.com/download/

- (Recommended) PLUX APIs 
https://bitalino.com/pyAPI/  
https://www.biosignalsplux.com/en/software/apis  

- (Recommended) Pynput library for Keyboard events listener  
https://pypi.org/project/pynput/  

##  2. Sensing platform documentation <a name="docs"></a>
- PLUX PZT respiration sensor  
http://bitalino.com/datasheets/PZT_Sensor_Datasheet.pdf  
https://www.biosignalsplux.com/datasheets/PZT_Sensor_Datasheet.pdf

##  3. Other useful resources in case of audio feedback<a name="resrc"></a>  
-Cecilia   
http://ajaxsoundstudio.com/software/cecilia/  

- loopMIDI  
https://www.tobias-erichsen.de/software/loopmidi.html

- Dexed  
https://asb2m10.github.io/dexed/

- <span style="color:red">M̵I̵D̵O̵ ̵M̵I̵D̵I̵ ̵P̵y̵t̵h̵o̵n̵ ̵l̵i̵b̵r̵a̵r̵y̵ ̵ </span>  
https://mido.readthedocs.io/en/latest/

##  4. Configuration <a name="config"></a>  
1. Pair your biosignalsplux device with your computer

2. Use OpenSignals(r) software to enable the device and launch acquisition, choosing the right channels and sampling rate

3. Set the TCP integratiDownload and open this Processing sketch to monitor inputs
OSCDataPlotter.zip
on checkbox ON and default port. 

4. When launched, make sure the websocket connects to your local TCP/IP. IP can be manually input in the code.

##  5. OSC Output <a name="osc"></a>  
Download and open this Processing sketch to monitor inputs
[OSCDataPlotter.zip](https://gitlab.com/weselle/riot-serverbit/uploads/1a2d9ec4d86e649aac9a0268e8c3ce8d/OSCDataPlotter.zip)

![Screen_Shot_2018-11-05_at_12.13.39_PM](https://gitlab.com/weselle/riot-serverbit/uploads/0890fb9607a513424bfab356f1c140ad/Screen_Shot_2018-11-05_at_12.13.39_PM.png)

Check that the `receiveDataOnOSCPort` and `ipAddress` variables are set correctly according to the device configuration

***

##  Other projects
SyncXsens  
http://tinyurl.com/syncxsens  
