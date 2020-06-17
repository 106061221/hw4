import matplotlib.pyplot as plt
import numpy as np
import serial


import paho.mqtt.client as paho

import time

b="0000"

mqttc = paho.Client()


# Settings for connection

host = "localhost"

topic= "Mbed"

port = 1883


# Callbacks

def on_connect(self, mosq, obj, rc):

    print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):
    global b
#    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");
    b = str(msg.payload)


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

t = np.arange(0,20,1)
td = np.arange(0,20,1)

for x in range(-2, 20):
    mqttc.loop()
    td[x]=int(b[2])
#    print(b[2])
    time.sleep(1)
fig, ay = plt.subplots(1, 1)
ay.plot(t,td,) # plotting the spectrum
ay.set_xlabel('Time')
ay.set_ylabel('Tilt')
plt.show()