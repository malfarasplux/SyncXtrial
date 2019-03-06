


import asyncio, time, sys
import websockets, json
import numpy as np
import syncmetrics as syncm
from numpy_ringbuffer import RingBuffer

from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client


# In[2]:


# OSC output config
local_ip = '127.0.0.1'
local_port = 12000
output_address = '/results'
client = udp_client.SimpleUDPClient(local_ip, local_port)

#    Send to Processing/MAX/Etc...
def send_osc_bundle(*values):
    bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
    msg = osc_message_builder.OscMessageBuilder(address=output_address)
    # Test bundle outputs: 1, 2, 3, ...
    for val in values:
        print (val)
        msg.add_arg(val)
        bundle.add_content(msg.build())
        bundle = bundle.build()
    client.send(bundle)
    
def output_individual(data, labels):
    data = json.loads(data)
    printJSON(data)
    bundle = osc_bundle_builder.OscBundleBuilder(
        osc_bundle_builder.IMMEDIATELY)

    for label in labels:
        output_address += self.device_number + "/bitalino/" + label
        msg = osc_message_builder.OscMessageBuilder(
            address=output_address)
        msg.add_arg(arg_to_add)
        msg.build()
        client.send(msg)


# In[3]:


class Session:
    device_data = json.dumps({})
    uri = 'ws://localhost:8000'
    ws_timeout = 5.0
    num_users = 2
    
    # to do processing in windoes 
    fs=1000
    buffer_W=150
    win_size=15*fs
    window_A = np.zeros(win_size)
    window_B = np.zeros(win_size)
    no_buffer=int(win_size/buffer_W)
    buffers = RingBuffer(capacity=no_buffer, dtype=(float, num_users))

    def calculate_features(self):
        device_data = json.loads(self.device_data)
        self.buffers.appendleft([device_data["A1"][0], device_data["A2"][0]])
        
        if self.buffers.shape[0] > self.no_buffer-1:
            buff_A = np.array([i[0] for i in np.array(self.buffers)])
            buff_B = np.array([i[1] for i in np.array(self.buffers)])
            result_1=syncm.lin_reg_r_metric(buff_A, buff_B)
            result_2=syncm.cos_similarity(buff_A, buff_B).flat[0]

            #add results here
            results = [result_1, result_2]
#             print(results)
            send_osc_bundle(results)

    async def ServerBIT_recieve(self, uri):
        async with websockets.connect(uri) as websocket:
            while True:
                self.device_data = await websocket.recv()
                self.calculate_features()
                await asyncio.sleep(0.0)
                
    def run(self):
        uri = self.uri
        print("Serving on {}".format(uri))
        try:
            asyncio.get_event_loop().run_until_complete(
                self.ServerBIT_recieve(uri))
        except Exception as e:
            print(e)
            pass
        finally:
            print("no connection, try again")
            exit


# In[4]:


session = Session()
session.run()


# In[ ]:




