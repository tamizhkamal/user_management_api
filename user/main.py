import base64
import datetime
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from Auth.crud import get_current_active_user
from database import get_db
from user.crud import delete_user_data, update_user_data
from user.models import UserMaster, Project, Task
from user.schemas import UserCreate, ProjectCreate, TaskCreate, UserUpdate
from datetime import datetime
from datetime import datetime
import base64


router = APIRouter(prefix="/user")


@router.get("/all_user_data", tags=['User'])
async def all_user_data(db: Session = Depends(get_db)):
    data = db.query(UserMaster).all()
    return {'data':data}


@router.put("/image_update_data/{id}", tags=['User'])
async def image_update_data(user: UserMaster = Depends(get_current_active_user), image: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(UserMaster).filter(UserMaster.id == user.id).first()
    if not user:
        return {"message": "User not found"}
    image_data = await image.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    user.image = encoded_image
    db.commit()
    return {"message": "Image updated successfully", "user_id": id}


@router.get("/filter_user_data", tags=['User'])
async def filter_user_data(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserMaster).filter(UserMaster.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    projects = db.query(Project).filter(Project.user_id == user_id).all()
    tasks = []
    sub_tasks = []
    for project in projects:
        project_tasks = db.query(Task).filter(Task.project_id == project.id).all()
        tasks.extend(project_tasks)

    user_data = user.__dict__
    project_data = [project.__dict__ for project in projects]
    task_data = [task.__dict__ for task in tasks]
    # sub_task_data = [sub_task.__dict__ for sub_task in sub_tasks]

    return {
        "Message": "User data, associated projects, tasks, and sub-tasks fetched successfully",
        "user": user_data,
        "projects": project_data,
        "tasks": task_data
    }



@router.put("/update_user", tags=["User"])
async def update_user(id,userdata: UserUpdate, db: Session = Depends(get_db)):
    final_dict = update_user_data(id,userdata,db)
    print("result", final_dict)
    return final_dict  

@router.delete("/delete_user", tags=["User"])
async def delete_user(id,userdata: UserUpdate, db: Session = Depends(get_db)):
    final_dict = delete_user_data(id,userdata,db)
    print("result", final_dict)
    return final_dict  

@router.post("/create_project", tags=['Project'])
async def create_project(project: ProjectCreate, user: UserMaster = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        start_date = datetime.strptime(project.start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(project.end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        print(user,"<-------------- user")
        project_db = Project(
            name=project.name,
            start_date=start_date,
            end_date=end_date, 
            user_id=user.id,
            created_by=user.id,
            updated_by=user.id
        )
        
        db.add(project_db)
        db.commit()
        db.refresh(project_db)
        
        return {"Message": "Project created successfully", 'data': project_db}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.get("/all_project_data", tags=['Project'])
async def all_project_data(user: UserMaster = Depends(get_current_active_user),db: Session = Depends(get_db)):
    data = db.query(Project).all()
    return {'data':data}


@router.put("/update_project", tags=['Project'])
async def update_project(id:int,project: ProjectCreate, user: UserMaster = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = db.query(Project).filter(Project.id == id).first()
    try:
        start_date = datetime.strptime(project.start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(project.end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        print(user,"<-------------- user")
        data.name=project.name,
        data.start_date=start_date,
        data.end_date=end_date, 
        data.user_id=user.id,
        data.created_by=user.id,
        data.updated_by=user.id
        db.commit()        
        return {"Message": "Project updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.delete("/Delete_project", tags=['Project'])
async def Delete_project(id:int,user: UserMaster = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        data = db.query(Project).filter(Project.id == id).first()
        data.delete = True
        db.commit
        return {"Message": "Project Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    

@router.post("/create_task", tags=['Task'])
async def create_task(task: TaskCreate,user: UserMaster = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        sub_tasks_data = []
        if task.sub_tasks:
            for sub_task_data in task.sub_tasks:
                sub_task = {
                    "id": sub_task_data.id,
                    "sub_task_name": sub_task_data.sub_task_name,
                    "start_time": sub_task_data.start_time,
                    "end_time": sub_task_data.end_time,
                    "status": sub_task_data.status
                }
                sub_tasks_data.append(sub_task)
        
        task_db = Task(
            name=task.name,
            due=task.due,
            priority=task.priority,
            start_time=task.start_time,
            end_time=task.end_time,
            sub_tasks=sub_tasks_data,
            project_id=task.project_id,
            created_by = user.id

        )
        
        db.add(task_db)
        db.commit()
        db.refresh(task_db)
        
        return {"Message": "Task created successfully", 'data': task_db}
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the Task")    


@router.get("/all_task_data", tags=['Task'])
async def all_task_data(user: UserMaster = Depends(get_current_active_user),db: Session = Depends(get_db)):
    data = db.query(Task).all()
    return {'data':data}

@router.put("/update_task", tags=['Task'])
async def update_task(id: int, task: TaskCreate, user: UserMaster = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        # Retrieve the task from the database
        task_db = db.query(Task).filter(Task.id == id).first()
        
        if not task_db:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update the task fields
        task_db.name = task.name
        task_db.due = task.due
        task_db.priority = task.priority
        task_db.start_time = task.start_time
        task_db.end_time = task.end_time
        task_db.project_id = task.project_id
        
        # Update subtasks
        sub_tasks_data = []
        if task.sub_tasks:
            for sub_task_data in task.sub_tasks:
                sub_task = {
                    "id": sub_task_data.id,
                    "sub_task_name": sub_task_data.sub_task_name,
                    "start_time": sub_task_data.start_time,
                    "end_time": sub_task_data.end_time,
                    "status": sub_task_data.status
                }
                sub_tasks_data.append(sub_task)
        
        # Update the subtasks of the task
        task_db.sub_tasks = sub_tasks_data
        
        # Commit changes to the database
        db.commit()
        
        return {"Message": "Task Updated successfully", 'data': task_db}
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the Task")
    

@router.delete("/Delete_Task", tags=['Task'])
async def Delete_Task(id:int,user: UserMaster = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        data = db.query(Task).filter(Task.id == id).first()
        data.delete = True
        db.commit
        return {"Message": "Project Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
