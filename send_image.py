import paho.mqtt.client as mqtt
import json
import base64

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
publish_topic = "/imagetest1"
# publish_topic = f"/shift/{sitename}/{uname}/sensorvalues"
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
# client.connect("103.231.240.146", 11000)
client.connect("mqtt.eclipseprojects.io", 1883, 60)
print(client)
print(publish_topic)

image = "sample_image.jpg"
print(type(image))

with open(image, "rb") as f:
    imagestring = f.read()
    image_bytes = bytearray(imagestring)
    print(image_bytes)
    # image_bytes = base64.b64encode(f.read())
    # image_str = image_bytes.decode('ascii')
    # print(image_str)

client.publish(publish_topic, image_bytes, 0)
client.loop_forever()
