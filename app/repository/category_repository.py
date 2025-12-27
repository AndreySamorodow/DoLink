from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Category]:
        query = select(Category)
        result = await self.db.execute(query)
        return result.scalars().all()

    
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        query = select(Category).filter_by(id=category_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, category_data: CategoryCreate) -> Category:
        db_category = Category(**category_data.model_dump())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    