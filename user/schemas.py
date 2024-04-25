from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    email: str
    contact_number: str
    location: Optional[str] = None
    pincode: Optional[str] = None
    is_admin: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class UserBase(UserCreate):
    hashed_password: str

class UserResponse(BaseModel):
    data: List[UserBase]


class ProjectCreate(BaseModel):
    name: str
    start_date: str
    end_date: str
    user_id: int

class ProjectResponse(BaseModel):
    data: List[ProjectCreate]

    model_config = ConfigDict(from_attributes=True)  # Corrected version

    
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
    parent_id: Optional[int] = None
    project_id: int



class TaskItem(BaseModel):
    id: int
    name: str
    due: str
    priority: str
    start_time: str
    end_time: str
    project_id: int
    sub_tasks: Optional[List['TaskItem']] = []


class TaskResponse(BaseModel):
    data: List[TaskItem]



# Pydantic models for serialization
class TaskResponse(BaseModel):
    id: int
    name: str
    due: str
    priority: str

    model_config = ConfigDict(from_attributes=True)


class ProjectResponse(BaseModel):
    id: int
    name: str
    tasks: list[TaskResponse]

    model_config = ConfigDict(from_attributes=True)