# app/schemas/task.py

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    on_hold = "on_hold"
    cancelled = "cancelled"

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    status: TaskStatus = TaskStatus.in_progress

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    status: Optional[TaskStatus] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: int

    class Config:
        from_attributes = True
