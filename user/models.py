# models.py
import datetime
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy.orm import relationship

class UserMaster(Base):
    __tablename__ = "user_master"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50))
    email = Column(String(length=255), unique=True, index=True)
    contact_number = Column(String(length=20), unique=True, index=True)
    hashed_password = Column(String)
    access_token = Column(String)
    token_type = Column(String)
    otp = Column(String)
    image = Column(String)
    is_admin = Column(Boolean)
    delete = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, index=True)
    updated_by = Column(Integer, index=True)
    projects = relationship("Project", back_populates="user")  # Define relationship with Project

class Project(Base):
    __tablename__ = 'project_master'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    start_date = Column(Date)
    end_date = Column(Date)
    user_id = Column(Integer, ForeignKey('user_master.id'))
    delete = Column(Boolean)
    user = relationship("UserMaster", back_populates="projects")  # Define relationship with UserMaster
    created_by = Column(Integer, index=True)
    updated_by = Column(Integer, index=True)

class Task(Base):
    __tablename__ = 'task_master'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    due = Column(String)
    priority = Column(String)
    start_time = Column(String)  # Assuming start_time and end_time are strings
    end_time = Column(String)
    sub_tasks = Column(JSON)  # Storing subtasks as JSON
    delete = Column(Boolean)
    created_by = Column(Integer, ForeignKey('user_master.id'))
    project_id = Column(Integer, ForeignKey('project_master.id'))
    