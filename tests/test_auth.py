import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app factory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base  # Assuming you have a Base model to create test tables
from user.schemas import UserCreate, ProjectCreate  # Import your schemas
import datetime

# Create a new database engine for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use SQLite for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Fixture to create and yield a database session, and clean up afterwards."""
    Base.metadata.create_all(bind=engine)  # Create tables for the test database
    session = TestingSessionLocal()
    try:
        yield session  # Return the session to the test case
    finally:
        session.close()  # Close the session
        Base.metadata.drop_all(bind=engine)  # Clean up tables after test

@pytest.fixture(scope="module")
def client():
    """Fixture to create a test client for FastAPI."""
    # app_tour = app()  # Create your FastAPI app
    with TestClient(app) as c:
        yield c  # Return the client to the test cases
