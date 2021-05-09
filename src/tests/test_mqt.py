import paho.mqtt.client as mqtt
import json
import uuid
import logging
import os

# create console handler and set level to debug
logger = logging.getLogger()
consoleHandler = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

BROKER_ADDRESS = '123.209.90.112'
BROKER_PORT = 1883

# change for your application id in chirpstack
APPLICATION_ID = "1"


# PAHO MQTT CALLBACKS
def on_message(client, userdata, message):
    logger.info(f'Message received: {message.payload}')
    logger.info('Parsing Payload JSON...')

    # try and parse to Json
    json_data = json.loads(message.payload)

    if not isinstance(json_data, dict):
        return

    obj = json_data.get('object')

    if not obj:
        logging.warning('Parsed JSON did not contain "object".')

    else:
        logger.info('DeviceID : ', json_data.get('devEUI'))
        obj['APPLICATION_ID'] = APPLICATION_ID
        obj['devEUI'] = json_data['devEUI']

        json_data_str = json.dumps(obj)

        logger.info(f'Object: {json_data_str}')
        logger.info('Azure: sending message...')


# Connection to Chirpstack pub/sub broker
client = mqtt.Client()  # create new instance
client.on_message = on_message  # attach function to callback

logger.info('Connecting to pub/sub broker.')
client.connect(BROKER_ADDRESS, BROKER_PORT)  # connect to broker

logger.info('Broker: Subscribing to device rx topic')
client.subscribe('application/' + APPLICATION_ID + '/device/+/rx')

client.loop_forever()
