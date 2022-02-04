import paho.mqtt.client as mqtt
import json
import binascii
from io import BytesIO
import os

sitename = 'dlsau'
uname = 'testpi'
subscribe_topic = "/mqtt/abcdxyz"
mqttIP = "mqtt.eclipseprojects.io"
mqttPort = 1883
# mqttIP = "103.231.240.146"
# mqttPort = 11000

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

dest = 'images/'
create_path(dest)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic)
    # print(str(msg.payload))
    print()
    if msg.topic == subscribe_topic:
        print(msg.topic)
        # print(str(msg.payload))
        payload = json.loads(msg.payload)
        # print(payload)
        filename = payload['filename']
        print(filename)
    #     hostname = payload['hostname']
        with open(dest + '/' + filename, 'wb') as f:
            f.write(binascii.a2b_base64(payload['image_data']))
            print("image successfully received")


def on_publish(client, userdata, mid):
    print("Message published")

# mqtt client init
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(mqttIP, mqttPort)
client.subscribe(subscribe_topic)

client.loop_forever()
