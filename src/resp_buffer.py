
#Program ONLINE to explore Synchrony via 2 BITalino 1-axis RESP Sensors (A5, A6) and sound feedback
from __future__ import division

import socket
import json
import threading
import select
import queue
import pandas as pd
import numpy as np
import time
import syncmetrics as syncm

from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client

import asyncio

class bitalino_data(object):
    def __init__(self):
        self.channel_id = ['ind', 'da', 'db', 'dc', 'dd', 'RESP1','RESP2']
        self.nchannels = len(self.channel_id)
        self.data = []
    def val(self, ch_name):
        try :
            i = self.channel_id.index(ch_name)
            return self.data.values[:,i]
        except:
            print("Non-existent ch_name", ch_name)
            return np.array([-1])

# Global
bit1 = bitalino_data()
DATA = []
sigA=[]
sigB=[]
W_A=[]
W_B=[]

# OSC output Config
local_ip = '127.0.0.1'
local_port = 8888
output_address = '/0/result'
client = udp_client.SimpleUDPClient(local_ip, local_port)

def show_menu():
    for id in list(MENU_INPUT.keys()):
        print(str(id) + ' | ' + MENU_INPUT[id])

def server_request(action):
    if action == '0':
        print("Listing devices (print needed in code)")
        return 'devices'
    elif action == '1':
        return 'start'
    elif action == '2':
        return 'stop'
    else:
        return ''

# TCP client class
class TCPClient(object):
    def __init__(self):
        self.tcpIp = ''
        self.tcpPort = 5555
        self.buffer_size = 99999

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inputCheck = []
        self.outputCheck = []
        self.isChecking = False
        self.isAcquiring = False
        self.msgQueue = queue.Queue()
        self.txtFile = SaveAcquisition()

    def connect(self):
        self.socket.connect((self.tcpIp, self.tcpPort))
        self.outputCheck.append(self.socket)
        self.isChecking = True

    def start(self):
        thread = threading.Thread(target=self.msgChecker)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.isChecking = False
        self.socket.close()
    
#    Send to Processing/MAX/Etc...
    def send_osc(self, dev_id, values):
        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        msg = osc_message_builder.OscMessageBuilder(address=output_address)
        # Test bundle outputs: 1, 2, 3, ...
        print(values[0])
        for val in values:
            print (val)
            msg.add_arg(val)
            bundle.add_content(msg.build())
            bundle = bundle.build()
        client.send(bundle)

    def msgChecker(self):
        global bit1
        global DATA
        global sigA
        global sigB
        global W_A
        global W_B

        

        # to do processing in windoes 
        fs=1000
        buffer_W=150
        win_size=15*fs
        no_buffer=int(win_size/buffer_W)
        W_A = np.zeros(win_size)
        W_B = np.zeros(win_size)
        delta_t=0.1*fs
        j = 0
        
#        bit1 = bitalino_data()
        while self.isChecking:
            readable, writable, exceptional = select.select(self.inputCheck, self.outputCheck, self.inputCheck)
            for s in readable:
                message = s.recv(self.buffer_size)
                if not self.isAcquiring:
#                    print(message)
                    self.inputCheck = []
                    message = ""
                else:
                    # Print when acquiring (15@100Hz, 150@1000hz instances)
#                    print(message)
                    message = json.loads(message.decode('utf8'))
#                    print("json loaded")
#                    print(message)
                    message = message["returnData"]
                    if not self.txtFile.getHasHeader():
                        newLine = json.dumps(message) + "\n"
                        self.txtFile.addData(newLine)
                        print("json txt header")

                    else:
                        dataframe = []
                        for device in list(message.keys()):
                            dataframe.append(pd.DataFrame(message[device]))

                        # Convert the list into a pandas.core.frame.DataFrame
                        dataframe = pd.concat(dataframe, axis=1, ignore_index=True)
                        DATA = dataframe
#                        print(dataframe)
                        ## wait until you get the full window size 
                       # if dataframe


                        # Store and normalise data
                        bit1.data = dataframe
#                        bit1.RESP1 = (bit1.val("RESP1")-512)/1024
                        bit1.RESP1 = (bit1.val("RESP1"))
                        bit1.RESP2 = (bit1.val("RESP2"))
                        sigA = bit1.RESP1
                        sigB = bit1.RESP2
                        if j<no_buffer :
                            i = j % no_buffer
                            W_A[i*buffer_W:(i+1)*buffer_W]=sigA
                            W_B[i*buffer_W:(i+1)*buffer_W]=sigB
                            j = j+1

                        else :
                            W_A = np.roll(W_A,-buffer_W)
                            W_A[-buffer_W:] = sigA
                            
                            W_B = np.roll(W_B,-buffer_W)
                            W_B[-buffer_W:] = sigB
                            result_1=syncm.lin_reg_r_metric(W_A,W_B)
                            
                            #add results here
                            result.append(result_1)
                            print(result)
                            #forward to OSC bundle
                            self.send_osc(0, results)
                       
                        for line in dataframe.values:
                            self.txtFile.addData('\n')
                            self.txtFile.addData(",".join([str(x) for x in line]))

            for s in writable:
                try:
                    next_msg = self.msgQueue.get_nowait()
                except queue.Empty:
                    pass
                else:
                    print("send ")
                    self.socket.send(next_msg.encode('utf-8'))

            for s in exceptional:
                print("exceptional ", s)

    def addMsgToSend(self, data):
        self.msgQueue.put(data)
        if self.socket not in self.outputCheck:
            self.outputCheck.append(self.socket)
        if self.socket not in self.inputCheck:
            self.inputCheck.append(self.socket)

    def setIsAcquiring(self, isAcquiring):
        self.isAcquiring = isAcquiring
        if self.isAcquiring:
            self.txtFile = SaveAcquisition()
            self.txtFile.start()
        else:
            self.txtFile.stop()

class SaveAcquisition(object):
    def __init__(self):
        self.fileTxt = None
        self.hasHeader = False

    def start(self):
        self.fileTxt = open("mytcpRESP_Acquisition.txt", "w")

    def addData(self, data):
        self.fileTxt.write(data)
        self.hasHeader = True

    def stop(self):
        self.fileTxt.close()

    def getHasHeader(self):
        return self.hasHeader


##################################################################################################
##################################################################################################
# BITalino OpenSignals(r) TCP client to get acquisition data


if __name__ == "__main__":
    MENU_INPUT = {1: 'Acquisition',
                  2: 'Stop',
                  3: 'Exit'
                  }
    try:
        thread_list = []
        CONNECTION = TCPClient()
        CONNECTION.connect()
        CONNECTION.start()

        while True:
            show_menu()
            user_action = str(input('Acquisition(1), Stop(2), Exit(3): '))
            if user_action == '1':
                CONNECTION.setIsAcquiring(True)

            elif user_action == '2':
                CONNECTION.setIsAcquiring(False)


            elif user_action == '3':
                try:
                    CONNECTION.setIsAcquiring(False)
                except:
#                    print("set acquire False not possible")
                    pass
                CONNECTION.stop()
                break
            new_msg = server_request(user_action)
            CONNECTION.addMsgToSend(new_msg)

        print("END")
    finally:
        pass
