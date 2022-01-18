import paho.mqtt.client as mqtt
import json
import binascii

dest = 'csv/'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    if msg.topic == subscribe_topic:
        payload = json.loads(msg.payload)
        print(payload)
        filename = payload['filename']
        with open(dest + filename, 'wb') as f:
            f.write(binascii.a2b_base64(payload['csv_data']))
            print("csv successfully received")
        # csv_str = payload["c2"].encode('ascii')
        # csv_bytes = base64.b64encode(csv_str)
        # csv = open('recv_csv.jpg', 'wb')
        # csv.write(csv_bytes)
        # csv.close()

def on_publish(client, userdata, mid):
    print("Message published")

# mqtt client init
client = mqtt.Client()
subscribe_topic = "/shift/DLSAU/master-pi/csvs"
# subscribe_topic = f"/shift/{sitename}/{uname}/sensorvalues"
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect("103.231.240.146", 11000)
# client.connect("mqtt.eclipseprojects.io", 1883, 60)
print(subscribe_topic)


client.subscribe(subscribe_topic)
client.loop_forever()
