import json
from fastapi.testclient import TestClient
import sys
import os
# Add the project root directory to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r'E:\\kamal backup\\zoonest\\crud_fastAPI-1\\main.py')))
from main import app
from main import app

client  = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    try:
        json_response = response.json()
    except json.decoder.JSONDecodeError as e:
        print(e, "<---------------------------- JSONDecodeError occurred")
        json_response = None

    if json_response is not None:
        assert json_response == {"message": "hello world..."}
    else:
        print("Response is not in JSON format")

def test_webhook_endpoint():
    payload = {
        "event": "task_created",
        "data": {
            "task_id": 123,
            "task_name": "Sample Task",
            "assigned_to": "John Doe",
            "due_date": "2024-04-20"
        }
    }
    
    response = client.post("/webhook", json=payload)
    try:
        json_response = response.json()
    except json.decoder.JSONDecodeError as e:
        print(e, "<---------------------------- JSONDecodeError occurred")
        json_response = None
    
    if json_response is not None:
        assert response.status_code == 200
        assert response.json() == {"message": "Webhook received and processed successfully"}
    else:
        print("Response is not in JSON format")