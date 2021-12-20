import paho.mqtt.client as mqtt
from time import sleep
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    # if msg.topic == "t1/t2":
    #     payload = json.loads(msg.payload)
    #     print(payload)
    # client.disconnect()

def on_publish(client, userdata, mid):
    print("Message published")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect("mqtt.eclipseprojects.io", 1883, 60)
# client.connect("103.231.240.146", 11000)
# "103.231.240.146", 11000
publish_topic = f"/shift/DLSAU/master-pi/sensorvalues"

# client.loop_forever()
client.subscribe(publish_topic)
client.loop_forever()



# while True:
#     data_out = json.dumps(data)
#     client.publish("t1/t2", data_out)
#     data['i'] += 1
#     data['j'] += 2
#     data['k'] += 3
#     sleep(5)
