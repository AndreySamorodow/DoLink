from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_password_hash, verify_user_reg_data
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def user_register_service(self, user_create_data: UserCreate) -> UserResponse:
        verify_user_reg_data(db=self.db, user_data=user_create_data)

        hashed_password = get_password_hash(user_create_data.password)

        user = User(
            name=user_create_data.name,
            email=user_create_data.email,
            hashed_password=hashed_password
        )
    
        saved_user = await self.user_repository.user_register(user)
    
        return UserResponse.model_validate(saved_user)
