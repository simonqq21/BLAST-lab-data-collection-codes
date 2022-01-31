import paho.mqtt.client as mqtt
import json
import binascii
from config import mqttIP, mqttPort
from io import BytesIO
import os
from config import create_path

dest = '/home/pi/images/'
create_path(dest)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    print(msg.payload)
    if msg.topic == subscribe_topic:
        payload = json.loads(msg.payload)
        print(payload)
        filename = payload['filename']
        with open(dest + filename, 'wb') as f:
            f.write(binascii.a2b_base64(payload['image_data']))
            print("image successfully received")


def on_publish(client, userdata, mid):
    print("Message published")

# mqtt client init
client = mqtt.Client()
subscribe_topic = "/shift/dlsau-kratky/dlsau-kratky0edge-1/images"
# subscribe_topic = f"/shift/{sitename}/{uname}/sensorvalues"
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(mqttIP, mqttPort)
# client.connect("mqtt.eclipseprojects.io", 1883, 60)
print(subscribe_topic)

client.subscribe(subscribe_topic)
client.loop_forever()
