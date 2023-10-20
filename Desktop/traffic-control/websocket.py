from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi import FastMQTT, MQTTConfig

app = FastAPI()
mqtt_subscriber = mqtt.Client()

with open("style.html", "r") as file:
    html = file.read()

async def func():
    mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic

    return {"result": True,"message":"Published" }

app = FastAPI()

mqtt_config = MQTTConfig()

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

@mqtt.subscribe("my/mqtt/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@mqtt.subscribe("my/mqtt/topic/#", qos=2)
async def message_to_topic_with_high_qos(client, topic, payload, qos, properties):
    print("Received message to specific topic and QoS=2: ", topic, payload.decode(), qos, properties)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

mqtt_config = MQTTConfig(host = "mqtt.mosquito.org",
    port= 1883,
    keepalive = 60,
    username="username",
    password="strong_password")


mqtt = FastMQTT(
    config=mqtt_config)