from typing import List, Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.auth.auth_function import get_user_id
from app.models.task import Task
from app.schemas.task import TaskCreate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Task]:
        stmt = select(Task).options(joinedload(Task.category), joinedload(Task.author))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    
    async def get_by_category(self, category_id: int) -> List[Task]:
        stmt = select(Task).options(joinedload(Task.category), joinedload(Task.author)).filter_by(category_id=category_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def get_by_id(self, task_id: int) -> Optional[Task]:
        stmt = select(Task).options(joinedload(Task.category), joinedload(Task.author)).filter_by(id=task_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_author_id(self, user_id):
        stmt = select(Task).options(joinedload(Task.category), joinedload(Task.author)).filter_by(author_id=user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def create(self, task_data: TaskCreate, user_id) -> Task:
        try:
            task_dict = task_data.model_dump()
            task_dict["author_id"] = user_id
                
            db_task = Task(**task_dict)
                
            self.db.add(db_task)
            await self.db.commit()  
            await self.db.refresh(db_task)
                
            return db_task
                
        except Exception as e:
            await self.db.rollback()  # Откат в случае ошибки
            raise e
        
    async def verification_user(self, task_id, user_id):
        stmt = select(Task).options(joinedload(Task.category), joinedload(Task.author)).filter_by(author_id=user_id, id=task_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def delete_task(self, task_id):
        stmt = delete(Task).where(Task.id == task_id)
        await self.db.execute(stmt)
        await self.db.commit()
