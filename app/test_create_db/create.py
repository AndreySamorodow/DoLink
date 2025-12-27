from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.models.category import Category
from app.schemas.category import CategoryCreate

#---------
#Router for adding categories (delete after adding!!!)
#---------

create_db_router = APIRouter(prefix="/add_category", tags=["create_db"])

@create_db_router.post("/d8dhn3d082o0olmnnn")
async def create_category(db: Annotated[AsyncSession, Depends(get_session)], category_data: CategoryCreate):

    db_category = Category(**category_data.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category
    