from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.schemas.task import TaskListResponse, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("", response_model=TaskListResponse)
async def get_all_tasks_router(db: Annotated[AsyncSession, Depends(get_session)]):
    service = TaskService(db)
    return await service.get_all_tasks()

@router.get("/category/{category_id}", response_model=TaskListResponse)
async def get_tasks_by_category_id_router(category_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    service = TaskService(db)
    return await service.get_tasks_by_category(category_id)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id_router(task_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    service = TaskService(db)
    return await service.get_task_by_id(task_id)
