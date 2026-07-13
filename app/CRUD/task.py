from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.schema.task import TaskCreate, TaskUpdate#schema bata task create garna ko lagi request ma k k pathaune vanera define gareko ho
from app.model.task import Task #model bata task ko table ko structure define gareko ho
from app.model.user import User #model bata user ko table ko structure define gareko ho
from app.schema.enum import TaskStatus #importing the TaskStatus enum from the app.schema.enum module and aliasing it as T for use in the Task model. This allows us to define the status column in the Task model using the predefined enum values for task status.

async def create_task(db: AsyncSession, task: TaskCreate, current_user= User) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        owner_id=current_user.id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_tasks(db: AsyncSession, current_user: User, skip: int, limit: int, status: TaskStatus) -> list[Task]:
    statement = select(Task).where(Task.owner_id == current_user.id).offset(skip).limit(limit)
    if status is not None:
        statement = statement.where(Task.status == status)
    result = await db.execute(statement)
    tasks = result.scalars().all()
    return tasks

async def update_task(db: AsyncSession, task: Task, task_update: TaskUpdate) -> Task:
    update_dict = task_update.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(task, key, value)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_task_by_id(db: AsyncSession, task_id: int, current_user: User) -> Task:
    result = await db.execute(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

async def delete_task(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()