# app/api/v1/tasks.py

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional

from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.core.dependencies import get_current_user
from app.services.task import create_task, get_tasks, update_task, delete_task
from app.schemas.user import UserOut

router = APIRouter()

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_new_task(task: TaskCreate, current_user: UserOut = Depends(get_current_user)):
    """
    Create a new task for the authenticated user.
    """
    created_task = await create_task(task, current_user.id)
    return created_task

@router.get("", response_model=List[TaskOut])
async def read_tasks(status: Optional[str] = None, current_user: UserOut = Depends(get_current_user)):
    """
    Retrieve tasks for the authenticated user, optionally filtered by status.
    """
    tasks = await get_tasks(current_user.id, status)
    return tasks

@router.put("/{task_id}", response_model=TaskOut)
async def update_existing_task(task_id: int, task_update: TaskUpdate, current_user: UserOut = Depends(get_current_user)):
    """
    Update a task by ID for the authenticated user.
    """
    updated_task = await update_task(task_id, task_update, current_user.id)
    if updated_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(task_id: int, current_user: UserOut = Depends(get_current_user)):
    """
    Delete a task by ID for the authenticated user.
    """
    success = await delete_task(task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return None
