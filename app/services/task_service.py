from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.category_repository import CategoryRepository
from app.repository.task_repository import TaskRepository
from app.schemas.task import TaskListResponse, TaskResponse


class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repository = TaskRepository(db)
        self.category_repository = CategoryRepository(db)


    async def get_all_tasks(self) -> TaskListResponse:
        tasks = await self.task_repository.get_all()
        tasks_response = [TaskResponse.model_validate(task) for task in tasks]
        return TaskListResponse(tasks=tasks_response, total=len(tasks_response))
    

    async def get_tasks_by_category(self, category_id: int) -> TaskListResponse:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found")
        
        tasks = await self.task_repository.get_by_category(category_id)
        tasks_response = [TaskResponse.model_validate(task) for task in tasks]
        return TaskListResponse(tasks=tasks_response, total=len(tasks_response))


    async def get_task_by_id(self, task_id: int) -> TaskResponse:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        return [TaskResponse.model_validate(task)]
    