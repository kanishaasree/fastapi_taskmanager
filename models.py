from typing import Optional
from sqlmodel import SQLModel, Field, Boolean

class Task(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, primary_key=True)
    task_name: str
    task_status: str

class CreateTask(SQLModel):
    task_name: str
    task_status: str

class TaskUpdate(SQLModel):
    task_name: Optional[str] = None
    task_status: Optional[str] = None

class TaskOut(SQLModel):
    task_id: int
    task_name: str
    task_status: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str

class UserCreate(SQLModel):
    username: str
    password: str

class UserLogin(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"