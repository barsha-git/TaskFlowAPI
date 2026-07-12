from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.schema.task import TaskCreate, TaskUpdate, TaskResponse
from app.CRUD.task import create_task, get_tasks, update_task
from app.model.task import Task
from dependency import get_db, get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskResponse])#crud ma vako function le list return dine vayera yah response model ma list define gareko ho
async def read_tasks(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = await get_tasks(db, current_user, skip, limit)
    return tasks

