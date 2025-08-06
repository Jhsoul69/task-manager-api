from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

# User
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

# Project
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectOut(ProjectCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# Task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = "todo"
    priority: Optional[int] = 3
    project_id: int
    assigned_to: Optional[int]

class TaskOut(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
