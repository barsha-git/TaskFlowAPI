from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.schema.task import TaskCreate, TaskUpdate#schema bata task create garna ko lagi request ma k k pathaune vanera define gareko ho
from app.model.task import Task #model bata task ko table ko structure define gareko ho
from app.model.user import User #model bata user ko table ko structure define gareko ho

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

async def get_tasks(db: AsyncSession, current_user: User, skip: int, limit: int) -> list[Task]:
    statement = select(Task).where(Task.owner_id == current_user.id).offset(skip).limit(limit)
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