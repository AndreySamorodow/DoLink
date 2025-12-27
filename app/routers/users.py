from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService


router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def user_register_router(db: Annotated[AsyncSession, Depends(get_session)], user_data: UserCreate):
    service = UserService(db)
    return await service.user_register_service(user_data)

