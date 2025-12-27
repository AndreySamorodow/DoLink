from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
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



    async def create(self, product_data: TaskCreate) -> Task:
        db_product = Task(**product_data.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    