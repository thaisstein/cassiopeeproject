from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import paho.mqtt.client as paho
import asyncio
import sys
app = FastAPI()

with open("style.html", "r") as file:
    html = file.read()


def on_message(ws, message):
    print(f"Received: {message}")

ws = FastAPI.Websocket.WebSocketApp("ws://localhost:8000/ws", on_message=on_message)
ws.run_forever()



