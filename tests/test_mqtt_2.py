import time
import paho.mqtt.client as paho
import json
import sys
import shutil
import traceback
import re
import subprocess
import glob
import datetime
import threading

# import argparse

VERBOSE = True
BROKER = "123.209.90.112"  # "127.0.0.1"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC2 = "application/+/device/+/rx"
# MQTT_TOPIC2 = "application/+/device/+/event/up"
# "application/+/device/+/event/up"

# TLS
tls_topic = threading.local()
tls_broker = threading.local()
tls_payload = threading.local()
tls_applicationName = threading.local()
tls_deviceName = threading.local()
tls_devEUI = threading.local()
tls_oldObj = threading.local()
tls_newTopic = threading.local()
tls_newObjStr = threading.local()

paho.Client.connected_flag = False
paho.Client.bad_connection_flag = False
client = paho.Client(
    "client-005")  # create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")


def main():
    client.tls_topic1 = MQTT_TOPIC2
    # client.tls_topic2 = MQTT_TOPIC2
    client.tls_broker = BROKER

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-v', action='store_true')
    # options = parser.parse_args()
    # VERBOSE = options.get('v', True)

    initBroker(client, BROKER)


# define callback
def on_messageEx(client, userdata, message):
    try:
        if VERBOSE:
            print()
            print('topic: {0}'.format(message.topic))
            print('payload: {0}'.format(message.payload))

        client.tls_payload = message.payload
        client.tls_json = json.loads(client.tls_payload)

        if VERBOSE:
            # clone object, use foll. properties:
            # "applicationName": "LHT65", -> device type, e.g. Temperature, Inklinometer
            print('applicationName: {0}'.format(client.tls_json['applicationName']))
            # "deviceName": "LHT65-FAussen",
            print('deviceName: {0}'.format(client.tls_json['deviceName']))
            # "devEUI": "a84041d251822b66",
            print('devEUI: {0}'.format(client.tls_json['devEUI']))
            print('oldObject: {0}'.format(client.tls_json['object']))

        client.tls_applicationName = client.tls_json['applicationName']
        client.tls_deviceName = client.tls_json['deviceName']
        client.tls_devEUI = client.tls_json['devEUI']

        client.tls_oldObj = client.tls_json['object']
        if 'id' in client.tls_json['object']:
            if VERBOSE: print('oldObject.id: {0}'.format(client.tls_json['object']['id']))
            client.tls_json['object']['id'] = client.tls_deviceName

        client.tls_newTopic = 'val/' + client.tls_applicationName + '/' + client.tls_deviceName
        if VERBOSE: print('newTopic: {0}'.format(client.tls_newTopic))

        client.tls_newObjStr = json.dumps(client.tls_oldObj)
        if VERBOSE: print('json_str: {0}'.format(client.tls_newObjStr))
        client.publish(client.tls_newTopic, client.tls_newObjStr)

    except Exception as e:
        print("json format error: {}".format(client.tls_newObjStr))
        print("type error: " + str(e))
        print(traceback.format_exc())


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        if VERBOSE: print("client is connected")
        # client.subscribe([(client.tls_topic1,0),(client.tls_topic2,0)])
        client.subscribe(client.tls_topic1, 0)
        if VERBOSE: print("client is subscribed to topic: {0}".format(client.tls_topic1))
        # if VERBOSE: print("client is subscribed to topic: {0}".format(client.tls_topic2))


def on_disconnect(client, userdata, rc=0):
    client.loop_stop()
    if VERBOSE: print("DisConnected result code " + str(rc))


# client.subscribe('application/' + APPLICATION_ID + '/device/+/rx')
def initBroker(client, broker_address):
    ######Bind function to callbacks
    client.on_disconnect = on_disconnect  # attach callback to on_disconnect function
    client.on_connect = on_connect  # bind callback to on_connect function
    paho.Client.connected_flag = False
    client.on_message = on_messageEx  # attach callback to on_message function

    #####
    try:
        print("connecting to broker ", broker_address)
        client.connect(broker_address)  # connect
        # client.loop_start() #start loop to process received messages
        client.loop_forever()
    except Exception as e:
        print("type error: " + str(e))
        print(traceback.format_exc())
        client.loop_stop()
        client.disconnect()  # disconnect


if __name__ == '__main__':
    main()
