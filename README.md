# SyncXtrial
Synchrony exploration through a sensing lens (PLUX sensors + OpenSignals + python)

[1. Tools required](#prereq)  
[2. Sensing platform documentation](#docs)  
[3. Extra resources](#resrc)  
[4. Configuration](#config)  

##  Code to assess synchrony between two signals <a name="syncassess"></a>
[syncmetrics.py](./src/sync_assess.py)  
[get_sync.py](./src/sync_assess.py)  



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
- loopMIDI  
https://www.tobias-erichsen.de/software/loopmidi.html

- Dexed  
https://asb2m10.github.io/dexed/

- <span style="color:red">M̵I̵D̵O̵ ̵M̵I̵D̵I̵ ̵P̵y̵t̵h̵o̵n̵ ̵l̵i̵b̵r̵a̵r̵y̵ ̵ </span>  
https://mido.readthedocs.io/en/latest/

##  4. Configuration <a name="config"></a>  
1. Pair your biosignalsplux device with your computer

2. Use OpenSignals(r) software to enable the device and launch acquisition, choosing the right channels and sampling rate

3. Set the TCP integration checkbox ON and default port. 

4. When launched, make sure the websocket connects to your local TCP/IP. IP can be manually input in the code.


***

##  Other projects
SyncXsens  
http://tinyurl.com/syncxsens  
