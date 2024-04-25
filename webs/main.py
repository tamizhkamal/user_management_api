import threading
import time
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, Response, WebSocket
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

# html = """

# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>WebSocket Chat</title>
#     <!-- Using Bootstrap for styling -->
#     <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
#     <style>
#         /* Chat container styling */
#         .chat-container {
#             display: flex;
#             flex-direction: column;
#             height: 90vh; /* Occupies 90% of the viewport height */
#             max-width: 600px; /* Limit width for smaller screens */
#             margin: 0 auto;
#             border: 1px solid #ccc;
#             border-radius: 10px;
#             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#             background: white;
#         }

#         /* Header bar styling */
#         .chat-header {
#             background: #005e54;
#             color: white;
#             padding: 15px;
#             text-align: center;
#             border-top-left-radius: 10px;
#             border-top-right-radius: 10px;
#         }

#         /* Main chat area styling */
#         .chat-body {
#             flex: 1;
#             overflow-y: auto; /* Allow vertical scrolling */
#             padding: 10px;
#             background: #f5f5f5;
#         }

#         /* Chat message styling */
#         .chat-message {
#             padding: 10px;
#             border-radius: 10px;
#             margin: 10px 0;
#             max-width: 60%; /* Limit width to make chat bubbles */
#         }

#         /* Sent message styling */
#         .message-sent {
#             background: #d1f4d1; /* Light green */
#             align-self: flex-end;
#             text-align: right;
#         }

#         /* Received message styling */
#         .message-received {
#             background: #fff; /* White */
#             align-self: flex-start;
#         }

#         /* Chat input area styling */
#         .chat-input {
#             display: flex;
#             align-items: center;
#             padding: 10px;
#             background: white;
#             border-top: 1px solid #ccc;
#             border-bottom-left-radius: 10px;
#             border-bottom-right-radius: 10px;
#         }

#         /* Input field styling */
#         .chat-input input {
#             flex: 1;
#             border: none;
#             outline: none;
#             padding: 10px;
#             font-size: 16px;
#         }

#         /* Send button styling */
#         .chat-input button {
#             background: #008a7c;
#             color: white;
#             border: none;
#             border-radius: 5px;
#             padding: 10px;
#             cursor: pointer;
#         }
#     </style>
# </head>
# <body>
#     <div class="chat-container">
#         <div class="chat-header">
#             WebSocket Chat - <span id="connection-status">Connecting...</span>
#         </div>
        
#         <div class="chat-body" id="chat-body">
#             <!-- Chat messages will be displayed here -->
#         </div>
        
#         <div class="chat-input">
#             <input type="text" id="messageText" placeholder="Type your message..." />
#             <button onclick="sendMessage(event)">Send</button>
#         </div>
#     </div>

#     <script>
#         var client_id = Date.now();
#         var ws;
#         var reconnectDelay = 3000; // 3 seconds delay for reconnecting

#         function connect() {
#             ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);

#             ws.onopen = function() {
#                 document.getElementById("connection-status").textContent = "Connected";
#             };

#             ws.onclose = function() {
#                 document.getElementById("connection-status").textContent = "Disconnected. Reconnecting...";
#                 setTimeout(connect, reconnectDelay); // Reconnect after 3 seconds
#             };

#             ws.onerror = function(error) {
#                 console.error("WebSocket error:", error);
#             };

#             ws.onmessage = function(event) {
#                 var chatBody = document.getElementById("chat-body");
#                 var message = document.createElement("div");
#                 message.className = "chat-message message-received";
#                 message.textContent = event.data;
#                 chatBody.appendChild(message);
#                 chatBody.scrollTop = chatBody.scrollHeight; // Scroll to the bottom
#             };
#         }

#         function sendMessage(event) {
#             event.preventDefault();
#             var input = document.getElementById("messageText");
#             if (input.value.trim() !== "") {
#                 ws.send(input.value.trim());
#                 var chatBody = document.getElementById("chat-body");
#                 var message = document.createElement("div");
#                 message.className = "chat-message message-sent";
#                 message.textContent = input.value.trim();
#                 chatBody.appendChild(message);
#                 chatBody.scrollTop = chatBody.scrollHeight; // Scroll to the bottom
#                 input.value = "";
#             }
#         }

#         connect(); // Connect WebSocket when the page loads
#     </script>
# </body>
# </html>


# """


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List


# Connection manager to manage active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

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
            await manager.send_personal_message(f"You : {data}", websocket)
            await manager.broadcast(f"Client #{client_id} : {data}")
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
# from anyio.to_thread import current_default_thread_limiter
from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool

# current_default_thread_limiter().total_tokens = 1000


def test():
    print(threading.current_thread().native_id)
    time.sleep(10)
    return 'ok'


@router.get("/read_root_pool")
async def read_root_pool():
    result = await run_in_threadpool(func=test)
    print(result)
    return {"Hello": "World"}

@app.get("/")
async def read_main():
    print("111111111111111111111")
    return {"msg": "Hello World"}

# Define the webhook endpoint
@router.post("/webhook")
async def handle_webhook(request: Request, payload: WebhookPayload):
    # Log or print the incoming data for debugging
    print("Webhook received:", payload)

    # Handle the incoming webhook data
    # You could process the data here and perform specific actions
    if payload.event == "task_created":
        task_data = payload.data
        # Process the task data (e.g., save to the database)
        print("Task data received:", task_data)
        # Return a successful response
        return {"status": "success", "message": "Webhook processed successfully"}

    # If the event type is unknown, return an error
    raise HTTPException(status_code=400, detail="Unknown event type")



