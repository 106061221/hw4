import serial

import matplotlib.pyplot as plt
import numpy as np
import serial

import time
import paho.mqtt.client as paho
mqttc = paho.Client()
host = "localhost"
topic= "Mbed"
port = 1883
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))
def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")
def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")
# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)


# XBee setting

serdev = '/dev/ttyUSB0'

s = serial.Serial(serdev, 9600)


s.write("+++".encode())

char = s.read(2)

print("Enter AT mode.")

print(char.decode())


s.write("ATMY 0x140\r\n".encode())

char = s.read(3)

print("Set MY 0x140.")

print(char.decode())


s.write("ATDL 0x240\r\n".encode())

char = s.read(3)

print("Set DL 0x240.")

print(char.decode())


s.write("ATID 0x1\r\n".encode())

char = s.read(3)

print("Set PAN ID 0x1.")

print(char.decode())


s.write("ATWR\r\n".encode())

char = s.read(3)

print("Write config.")

print(char.decode())


s.write("ATMY\r\n".encode())

char = s.read(4)

print("MY :")

print(char.decode())


s.write("ATDL\r\n".encode())

char = s.read(4)

print("DL : ")

print(char.decode())


s.write("ATCN\r\n".encode())

char = s.read(3)

print("Exit AT mode.")

print(char.decode())


print("start sending RPC")

Fs = 1.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = np.arange(0,20,Ts) # time vector; create Fs samples between 0 and 1.0 sec.
xd = np.arange(0,20,Ts) # signal vector; create Fs samples
yd = np.arange(0,20,Ts)
zd = np.arange(0,20,Ts)
td = np.arange(0,20,Ts)
amount=np.arange(0,20,1)

s.write("/getAcc/run\r".encode())
time.sleep(1)
for x in range(0, 20):

    # send RPC to remote
    
    # s.write("/getAcc/run\r".encode())

    #time.sleep(1)
    
    #s.write("/getAddr/run\r".encode())
    #time.sleep(0.5)
    s.write("/getAcc/run\r".encode())
    line=s.readline() # Read an echo string from K66F terminated with '\n'
    # print line
    xd[x] = float(line)
    line=s.readline()
    yd[x] = float(line)
    line=s.readline()
    zd[x] = float(line)
    line=s.readline()
    td[x] = float(line)
    line=s.readline()
    amount[x]=float(line)
    
    tilt=str(td[x])
    mesg = tilt
    mqttc.publish(topic, mesg)
    print(td[x])
#    time.sleep(0.1)

    time.sleep(1)



fig, ax = plt.subplots(3, 1)
ax[0].plot(t,xd, label='x')
ax[0].plot(t,yd, label='y')
ax[0].plot(t,zd, label='z')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Acc Vector')
ax[0].legend(loc='upper right')

ax[1].plot(t,amount,)
ax[1].set_xlabel('Time')
ax[1].set_ylabel('number')


ax[2].plot(t,td,) # plotting the spectrum
ax[2].set_xlabel('Time')
ax[2].set_ylabel('Tilt')

plt.show()



s.close()