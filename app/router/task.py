from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.schema.task import TaskCreate, TaskUpdate, TaskResponse
from app.CRUD.task import create_task, get_tasks, update_task
from app.model.task import Task
from app.dependency import get_db, get_current_user
from app.schema.enum import TaskStatus
from app.CRUD.task import get_task_by_id, delete_task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskResponse])#crud ma vako function le list return dine vayera yah response model ma list define gareko ho
async def read_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user), status: TaskStatus = None):
    tasks = await get_tasks(db, current_user, skip, limit, status)
    return tasks

@router.post("/", response_model=TaskResponse)
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    new_task = await create_task(db, task, current_user)
    return new_task

@router.get("/{task_id}", response_model=TaskResponse )
async def read_task(task_id: int, db: AsyncSession= Depends(get_db),current_user= Depends(get_current_user)):
    task= await get_task_by_id(db, task_id, current_user)
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    task = await get_task_by_id(db, task_id, current_user)
    updated_task = await update_task(db, task, task_update)
    return updated_task

@router.delete("/{task_id}", status_code=204)
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    task = await get_task_by_id(db, task_id, current_user)
    await delete_task(db, task)
    return None


