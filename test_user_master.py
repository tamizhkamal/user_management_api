from datetime import datetime
from pydantic import ValidationError
import pytest
from user_master_pydantic import UserMasterPydantic

@pytest.fixture
def valid_user_data():
    return {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "contact_number": "1234567890",
        "hashed_password": "hashed_password",
        "access_token": "access_token",
        "token_type": "bearer",
        "otp": "123456",
        "image": "profile.jpg",
        "is_admin": True,
        "delete": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": 1,
        "updated_by": 1
    }

def test_valid_user(valid_user_data):
    user = UserMasterPydantic(**valid_user_data)
    assert user

def test_invalid_user():
    invalid_user_data = {
        # Invalid data with missing required fields
        "username": "john_doe",
        "email": "john@example.com",
        "contact_number": "1234567890",
        "hashed_password": "hashed_password",
        "access_token": "access_token",
        "token_type": "bearer",
        "otp": "123456",
        "image": "profile.jpg",
        "is_admin": True,
        "delete": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": 1,
        "updated_by": 1
    }
    with pytest.raises(ValidationError):
        UserMasterPydantic(**invalid_user_data)
