import json
from typing import Annotated
from unittest.mock import patch
import warnings
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.testclient import TestClient
import sys
import os

import pytest

from database import get_db
from user.models import UserMaster

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r'E:\\kamal backup\\zoonest\\crud_fastAPI-1\\main.py')))


from main import app
# app = FastAPI()


client  = TestClient(app)

# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert "text/html" in response.headers["content-type"]

#     try:
#         json_response = response.json()
#     except json.decoder.JSONDecodeError as e:
#         print(e, "<---------------------------- JSONDecodeError occurred")
#         json_response = None

#     if json_response is not None:
#         assert json_response == {"message": "hello world..."}
#     else:
#         print("Response is not in JSON format")

# def test_read_main():
#     response = client.get("/")
#     print("Response Content: ------------> ", response.content)
#     assert response.status_code == 200
#     assert "text/html" not in response.headers["content-type"]  # FastAPI should return JSON, not HTML
#     # assert "application/json" in response.headers["content-type"], f"Unexpected Content-Type: {response.headers['content-type']}"


#     try:
#         json_response = response.json()
#     except json.JSONDecodeError:
#         json_response = None

#     assert json_response is not None, "Expected a JSON response"
#     assert json_response == {"message": "Hello world..."}

def test_root_endpoint():
    response = client.get("/")
    # warnings.warn(UserWarning("api v1, should use functions from v2"))
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

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
    assert response.status_code == 200
    try:
        json_response = response.json()
    except json.JSONDecodeError as e:
        print(e, "<---------------------------- JSONDecodeError occurred")
        json_response = None
    assert json_response is not None  # Ensure the response is not empty
    expected_response = {"status": "success", "message": "Webhook processed successfully"}  # Corrected expected output
    assert json_response == expected_response

# Dependency override to use the test database


app.dependency_overrides[Depends(get_db)] = get_db

# Test cases for creating a user
# @pytest.mark.asyncio
# def test_create_user():
#     # Sample user data
#     new_user = {
#         "username": "testuser",
#         "hashed_password": "testpassword",
#         "email": "testuser@example.com",
#         "contact_number": "1234567890",
#         "pincode": "123456",
#     }

#     # Send a POST request to the /AddUser endpoint
#     response = client.post("/AddUser", json=new_user)

#     # Assert that the response status code is 200
#     assert response.status_code == 200

#     # Check the response data to ensure the user was created successfully
#     data = response.json()
#     assert data["message"] == "User added successfully"
#     assert data["code"] == 200

#     # Verify the user was added to the database
#     db = next(get_db())
#     user_in_db = db.query(UserMaster).filter(UserMaster.email == "testuser@example.com").first()
#     assert user_in_db is not None
#     assert user_in_db.username == "testuser"
#     assert user_in_db.contact_number == "1234567890"


# working code 

# def test_create_user():
#     new_user = {
#         "username": "testuser",
#         "email": "k2k@gmail.com",
#         "contact_number": "172378297734",
#         "location": "trichy",
#         "pincode": "621117",
#         "is_admin": True,
#         "hashed_password": "1234"
#     }
    
#     response = client.post("/AddUser", json=new_user)
#     assert response.status_code == 200
#     data = response.json()
#     assert "message" in data and data["message"] == "User added successfully"
#     assert "code" in data and str(data["code"]) == "200"
#     assert "result" in data
#     assert "username" in data["result"] and data["result"]["username"] == "testuser"

@pytest.fixture
def setup_user(self):
        user = mixer.blend(User, email='a@a.com')
        user.set_password('1')
        user.save()
        return user


def test_create_item():
    response = client.post(
        "/create_task",
        headers={"X-Token": "coneofsilence"},
        json={
        "name": "login data",
        "due": "2",
        "priority": "high",
        "start_time": "12:29",
        "end_time": "03:00",
        "parent_id": 0,
        "project_id": 1,
    },
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": "login data",
        "due": "2",
        "priority": "high",
        "start_time": "12:29",
        "end_time": "03:00",
        "parent_id": 0,
        "project_id": 1,
    }

    # response = client.post("/create_task", json=payload)  
    # if x_token != fake_secret_token:
    #     raise HTTPException(status_code=400, detail="Invalid X-Token header")
    # assert response.status_code == 200
    # data = response.json()

    # assert "message" in data and data["message"] == "Task created successfully"
    # assert "code" in data and data["code"] == 200
    # assert "result" in data

    # return response


