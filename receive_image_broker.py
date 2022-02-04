import paho.mqtt.client as mqtt
import json
import binascii
from config import mqttIP, mqttPort
from io import BytesIO
import os
from config import create_path

dest = '/home/pi/images/'
# dest = 'images/'
create_path(dest)
hostnames = ["dlsau-dft0edge-1",
    "dlsau-dft0edge-2",
    "dlsau-dft0edge-3",
    "dlsau-kratky0edge-1",
    "dlsau-kratky0edge-2"]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    if msg.topic in subscribe_topics:
        print(msg.topic)
        payload = json.loads(msg.payload)
        filename = payload['filename']
        hostname = payload['hostname']
        with open(dest + hostname + '/' + filename, 'wb') as f:
            f.write(binascii.a2b_base64(payload['image_data']))
            print("image successfully received")

    # print(msg.topic)
    # print(str(msg.payload))
    # print()
    # if msg.topic == subscribe_topic:
    #     print(msg.topic)
    #     print(str(msg.payload))
    #     print()
    #     payload = json.loads(msg.payload)
    #     print(payload)
    #     filename = payload['filename']
    #     hostname = payload['hostname']
    #     with open(dest + hostname + '/' + filename, 'wb') as f:
    #         f.write(binascii.a2b_base64(payload['image_data']))
    #         print("image successfully received")


def on_publish(client, userdata, mid):
    print("Message published")

# mqtt client init
client = mqtt.Client()
client.connect(mqttIP, mqttPort)

subscribe_topics = []
for hostname in hostnames:
    create_path(dest + hostname)
    subscribe_topics.append("/shift/dlsau-kratky/{hostname}/images".format(hostname=hostname))

for topic in subscribe_topics:
    client.subscribe(topic)

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.loop_forever()
