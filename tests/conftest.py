# conftest.py in the tests folder

import pytest
from fastapi.testclient import TestClient
from main import app  # Adjust to your app import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base  # Assuming you have a Base model
from user.schemas import UserCreate, ProjectCreate
import datetime
from sqlalchemy.orm import declarative_base

PROJECT_NAME:str = "Datamoo.Ai"
PROJECT_VERSION: str = "1.0.0"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "1234"
POSTGRES_SERVER = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "zoonest_api_db"
   
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@pytest.fixture(scope="function")
def db():
    """Fixture to create and yield a database session, and clean up afterwards."""
    Base.metadata.create_all(bind=engine)  # Create tables for the test database
    session = SessionLocal()
    try:
        yield session  # Return the session to the test case
    finally:
        session.close()  # Close the session
        Base.metadata.drop_all(bind=engine)  # Clean up tables after test

@pytest.fixture(scope="module")
def client():
    """Fixture to create a test client for FastAPI."""
    # app_rout = app()  # Create your FastAPI app
    with TestClient(app) as c:
        yield c  # Return the client to the test cases
