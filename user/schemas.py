from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    contact_number: str
    hashed_password: str
    location: Optional[str] = None
    pincode: Optional[str] = None
    is_admin: Optional[bool] = None

class ProjectCreate(BaseModel):
    name: str
    start_date: str
    end_date: str
    user_id: int
    # image: Optional[UploadFile] = None
    
class UserUpdate(BaseModel):
    username: str
    contact_number: str
    
class SubTask(BaseModel):
    id: int
    sub_task_name: str
    start_time: str
    end_time: str
    status: str

class TaskCreate(BaseModel):
    name: str
    due: str
    priority: str
    start_time: str
    end_time: str
    sub_tasks: Optional[List[SubTask]] = None  # Optional list of subtasks
    project_id: int
