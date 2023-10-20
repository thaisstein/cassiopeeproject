from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException, Form

from fastapi.security import OAuth2PasswordBearer
import subprocess
import httpx

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



connected_websockets = []


# add a websocket to keep track of the clients
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)  # Add the connected client to the list
    try:
        while True:
            data = await websocket.receive_text()
            # Handle WebSocket messages and RabbitMQ publishing here
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)  # Remove the client when they disconnect


@app.get("/", response_class=HTMLResponse)
def get_subscribe_page(request: Request):
    # HTML form to subscribe
    return FileResponse("firstpage.html")

@app.post("/subscribe")
async def subscribe_to_rabbitmq():
    # Run emit_log.py to subscribe to RabbitMQ
    subprocess.call(["python3", "emit_log.py", "Subscribed to RabbitMQ"])
    #acho q aqui que vai as condicoes da BD
    return FileResponse("subscription.html")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    connected_websockets = get_connected_websockets()
    print("Connected Websockets:", connected_websockets)
