
# coding: utf-8

# In[1]:


from pythonosc import dispatcher
from pythonosc import osc_server


# In[2]:


def bitalino_input_handler(unused_addr, *values):
    list(values)
    print(values)


# In[3]:


dispatcher = dispatcher.Dispatcher()
dispatcher.map("/*/bitalino", bitalino_input_handler)


# In[4]:


ip = 'localhost'
port = 8000

server = osc_server.ThreadingOSCUDPServer(
  (ip, port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

