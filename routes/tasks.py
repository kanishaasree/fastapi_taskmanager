from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import Task, CreateTask, TaskOut, TaskUpdate
from authentic.dependencies import get_current_user
from services.notification import send_notification

router = APIRouter()

@router.get("/tasks", response_model=List[TaskOut])
async def list_tasks(
    session: AsyncSession = Depends(get_session),

):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return tasks

@router.post("/tasks")
async def create_task(
    task: CreateTask, 
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
  
    new_task = Task(task_name=task.task_name, task_status=task.task_status)
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    
    background_tasks.add_task(send_notification, task.task_name)

    return {"message": "Task created successfully", "task": new_task}

@router.patch("/tasks/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: AsyncSession = Depends(get_session),

):
    result = await session.execute(select(Task).where(Task.task_id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    
):
    result = await session.execute(select(Task).where(Task.task_id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(db_task)
    await session.commit()
    return {"message": f"Task with ID {task_id} deleted successfully"}



# @router.get("/github/{username}")
# async def get_github_user(username: str):
#     url = f"https://api.github.com/users/{username}"
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, timeout=10.0)
#         except httpx.RequestError as e:
#             raise HTTPException(status_code=503, detail=f"Network error: {e}")
#     if response.status_code == 404:
#         raise HTTPException(status_code=404, detail="GitHub user not found")
#     if response.status_code != 200:
#         raise HTTPException(status_code=502, detail=f"GitHub API error: {response.status_code}")

#     data = response.json()
#     return {
#         "login": data.get("login"),
#         "name": data.get("name"),
#         "public_repos": data.get("public_repos"),
#         "followers": data.get("followers"),
#         "following": data.get("following"),
#         "bio": data.get("bio"),
#         "html_url": data.get("html_url"),
#     }
