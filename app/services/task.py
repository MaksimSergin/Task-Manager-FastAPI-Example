# app/services/task.py

from typing import Optional, List

from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.db.session import db

async def create_task(task: TaskCreate, user_id: int) -> TaskOut:
    """
    Creates a new task for a given user.
    """
    query = """
    INSERT INTO tasks (title, description, status, user_id)
    VALUES ($1, $2, $3, $4)
    RETURNING id, title, description, status, user_id
    """
    record = await db.fetchrow(query, task.title, task.description, task.status, user_id)
    return TaskOut(**record)

async def get_tasks(user_id: int, status: Optional[str] = None) -> List[TaskOut]:
    """
    Retrieves tasks for a user, optionally filtered by status.
    """
    if status:
        query = """
        SELECT id, title, description, status, user_id 
        FROM tasks 
        WHERE user_id = $1 AND status = $2
        ORDER BY id DESC
        """
        records = await db.fetch(query, user_id, status)
    else:
        query = """
        SELECT id, title, description, status, user_id 
        FROM tasks 
        WHERE user_id = $1
        ORDER BY id DESC
        """
        records = await db.fetch(query, user_id)
    return [TaskOut(**record) for record in records]

async def update_task(task_id: int, updates: TaskUpdate, user_id: int) -> Optional[TaskOut]:
    """
    Updates a task's details.
    """
    query = "SELECT * FROM tasks WHERE id = $1 AND user_id = $2"
    existing_task = await db.fetchrow(query, task_id, user_id)
    if not existing_task:
        return None

    update_query = """
    UPDATE tasks 
    SET title = COALESCE($1, title),
        description = COALESCE($2, description),
        status = COALESCE($3, status)
    WHERE id = $4
    RETURNING id, title, description, status, user_id
    """
    updated_record = await db.fetchrow(update_query, updates.title, updates.description, updates.status, task_id)
    return TaskOut(**updated_record) if updated_record else None

async def delete_task(task_id: int, user_id: int) -> bool:
    """
    Deletes a task if it exists and belongs to the user.
    """
    query = "SELECT id FROM tasks WHERE id = $1 AND user_id = $2"
    existing_task = await db.fetchrow(query, task_id, user_id)
    if not existing_task:
        return False

    delete_query = "DELETE FROM tasks WHERE id = $1"
    await db.execute(delete_query, task_id)
    return True
