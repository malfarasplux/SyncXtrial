# SyncXtrial
Synchrony exploration through a sensing lens (PLUX sensors + OpenSignals + python)

[1. Tools required](#prereq)  
[2. Sensing platform documentation](#docs)  
[3. Extra resources](#resrc)  
[4. Configuration](#config)  

##  Code to assess synchrony between two signals <a name="syncassess"></a>
[sync_assess](./src/sync_assess.py)


##  1. Tools required <a name="prereq"></a>
- PLUX biosignalsplux + 2xPZT respiration sensors  
https://www.biosignalsplux.com/en/explorer

- Pyhton (v > 3.5)  
https://www.python.org/downloads/

- PLUX OpenSignals (r)evolution Software  
https://www.biosignalsplux.com/en/software  

- MIDO MIDI Python library  
https://mido.readthedocs.io/en/latest/

- (Recommended) Anaconda + Python  
 https://www.anaconda.com/download/

- (Recommended) biosignalsplux API  
https://www.biosignalsplux.com/en/software/apis  

- (Recommended) Pynput library for Keyboard events listener  
https://pypi.org/project/pynput/


##  2. Sensing platform documentation <a name="docs"></a>
- biosignalsplux PZT respiration sensor    
https://www.biosignalsplux.com/datasheets/PZT_Sensor_Datasheet.pdf

##  3. Other useful resources <a name="resrc"></a>  
- loopMIDI  
https://www.tobias-erichsen.de/software/loopmidi.html

- Dexed  
https://asb2m10.github.io/dexed/

##  4. Configuration <a name="config"></a>  
1. Pair your biosignalsplux device with your computer

2. Use OpenSignals(r) software to enable the device and launch acquisition, choosing the right channels and sampling rate

3. Set the TCP integration checkbox ON and default port. 

4. When launched, make sure the websocket connects to your local TCP/IP. IP can be manually input in the code.


***

##  Other projects
SyncXsens  
http://tinyurl.com/syncxsens  
