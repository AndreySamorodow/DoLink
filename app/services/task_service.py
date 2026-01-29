from datetime import datetime
from fastapi import Depends, HTTPException, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_function import get_token
from app.models.proposals import Proposal
from app.repository.category_repository import CategoryRepository
from app.repository.proposal_repository import ProposalRepository
from app.repository.task_repository import TaskRepository
from app.repository.user_repository import UserRepository
from app.schemas.proposal import ProposalCreate, ProposalResponse
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse
from app.database.dao import UserDao
from app.config import settings


class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repository = TaskRepository(db)
        self.category_repository = CategoryRepository(db)
        self.user_repository = UserRepository(db)
        self.proposal_repository = ProposalRepository(db)

    async def verification(self, task_id, user_id):
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if not await self.task_repository.verification_user(task_id, user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

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
        
        return TaskResponse.model_validate(task)
    
    async def get_task_by_author_id(self, user_id):
        tasks = await self.task_repository.get_by_author_id(user_id)
        tasks_response = [TaskResponse.model_validate(task) for task in tasks]
        return TaskListResponse(tasks=tasks_response, total=len(tasks_response))


    async def create_task(self, task_data: TaskCreate, user_id):
        category = await self.category_repository.get_by_id(task_data.category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")

        task = await self.task_repository.create(task_data, user_id)
        return TaskResponse.model_validate(task)



    async def respond_task(self, task_id: int, user_id: int, proposal_data: ProposalCreate) -> ProposalResponse:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The task does not exist")
        
        proposal_exists = await self.proposal_repository.get_proposal_exists(task_id, user_id)
        if proposal_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already responded to this task.")

        proposal = await self.proposal_repository.create(task_id, user_id, proposal_data)
        return ProposalResponse.model_validate(proposal)
        
    async def delete_task(self, task_id):
        await self.task_repository.delete_task(task_id)
        await self.proposal_repository.set_status_archived(task_id)
        raise HTTPException(status_code=status.HTTP_200_OK)

    
