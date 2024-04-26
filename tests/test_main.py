import json
from typing import Annotated
from unittest.mock import patch
import warnings
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.testclient import TestClient
import sys
import os
import pytest
from Auth.schemas import User
from database import get_db
from dependencies import get_data_hash
from user.models import Project, UserMaster
from main import app
from sqlalchemy.orm import Session

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), r'E:\\kamal backup\\zoonest\\crud_fastAPI-1\\main.py')))

client  = TestClient(app)


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


# app.dependency_overrides[Depends(get_db)] = get_db

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

def test_user_login(db: Session):
    # Password and hash function
    normal_password = "1234"
    hashed_pwd = get_data_hash(normal_password)  # Adjust according to your security module

    # Headers for JSON content
    headers = {
    "Content-Type": "application/json",
    }



    # Add a user to the database with a hashed password
    user_data = UserMaster(
        username="testuser",
        hashed_password=hashed_pwd,
        email="kam71al1s7haaksm@example.com"
    )
    db.add(user_data)
    db.commit()

    # Prepare the payload for login
    payload = {
    "username": "kamal",
    "password": '1234',
    }
    print("Sending payload:", payload)
    # response = client.post("/Auth/token", headers=headers, json=payload)    # Ensure that we get a successful response
    response = client.post("/Auth/token", headers=headers, json=payload)
    print("Response status code:", response.status_code)
    print("Response content:", response.json())

# def test_user_login(client, db):
#     """Test user login and token generation."""
#     # Create a hashed password
#     plaintext_password = "1234"
#     hashed_password = get_data_hash(plaintext_password)  # Hash the plaintext password

#     # Create a user with the hashed password
#     user_data = UserMaster(
#         username="testuser",
#         hashed_password=hashed_password,
#         email="te1231st@example.com"
#     )
#     db.add(user_data)
#     db.commit()

#     # Test login with the plaintext password (this will be hashed in the login process)
#     response = client.post(
#         "/Auth/token",
#         data={"username": "testuser", "password": plaintext_password}  # Use the plaintext password here
#     )
#     assert response.status_code == 200
#     assert "access_token" in response.json()  # Validate the token is returned
#     token = response.json()["access_token"]

#     # Test project creation with the obtained token
#     headers = {"Authorization": f"Bearer {token}"}
#     project_data = {
#         "name": "Test Project",
#         "start_date": "01/01/2024",
#         "end_date": "31/12/2024"
#     }
#     response = client.post("/create_project", headers=headers, json=project_data)
#     assert response.status_code == 200
#     assert response.json()["Message"] == "Project created successfully"