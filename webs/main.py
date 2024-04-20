import threading
import time
from fastapi import BackgroundTasks, FastAPI, Response, WebSocket
from fastapi import APIRouter
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import concurrent.futures
import requests

router = APIRouter(tags=['Web'])


@router.get("/test")
async def test():
    return


from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel

class WebhookPayload(BaseModel):
    event: str
    data: dict


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


# web_hooks 

@router.post("/web_hook")
async def receive_webhook(payload: WebhookPayload, response: Response):
    # Process the received webhook payload
    event = payload.event
    data = payload.data

    # Print the received event and data
    print(f"Received webhook event: {event}")
    print(f"Webhook data: {data}")

    # Forward the payload to another endpoint
    try:
        response = requests.post("https://webhook.site/5940b0a2-5914-47e8-9df4-ad250ecd755a", json=payload.dict())
        response.raise_for_status()
        print("Webhook forwarded successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        response.status_code = 500
        return {"Error": "Failed to forward webhook"}
    
    return {"message": "Webhook received and processed successfully"}




# thread_pool
from anyio.to_thread import current_default_thread_limiter
from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool

current_default_thread_limiter().total_tokens = 1000


def test():
    print(threading.current_thread().native_id)
    time.sleep(10)
    return 'ok'


@router.get("/read_root_pool")
async def read_root_pool():
    result = await run_in_threadpool(func=test)
    print(result)
    return {"Hello": "World"}