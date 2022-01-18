import paho.mqtt.client as mqtt
import json
import binascii
from io import BytesIO
import os

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    # if msg.topic == "t1/t2":
    #     payload = json.loads(msg.payload)
    #     print(payload)

def on_publish(client, userdata, mid):
    print("Message published")

# mqtt client init
client = mqtt.Client()
# publish_topic = "/imagetest1"
publish_topic = "/shift/DLSAU/master-pi/csvs"
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect("103.231.240.146", 11000)
# client.connect("mqtt.eclipseprojects.io", 1883, 60)
print(client)
print(publish_topic)

for filename in os.listdir('csv/'):
    if filename.endswith(('.csv',)):
        print(filename)
        with open('csv/' + filename, "rb") as f:
            # csv_bytes = BytesIO(f.read())
            csv_data = binascii.b2a_base64(f.read()).decode()

        data = {'filename': filename, 'csv_data': csv_data}
        jsondata = json.dumps(data)
        # client.publish(publish_topic, csv_bytes.read(), 0)
        client.publish(publish_topic, jsondata, 0)
client.loop_forever()
