from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_function import get_user_id
from app.database.database import get_session

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.task_service import TaskService
from app.services.user_service import UserService


router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def user_register_router(db: Annotated[AsyncSession, Depends(get_session)], user_data: UserCreate):
    service = UserService(db)
    return await service.user_register_service(user_data)


@router.post("/login", response_model=UserResponse)
async def user_login_router(db: Annotated[AsyncSession, Depends(get_session)], user_data: UserLogin, response: Response):
    service = UserService(db)
    return await service.user_login_service(user_data, response)


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("LinkDo_access_token")


@router.get("/profile/my_task")
async def get_my_task_router(db: Annotated[AsyncSession, Depends(get_session)], user_id = Depends(get_user_id)):
    service = TaskService(db)
    return await service.get_task_by_author_id(user_id)

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_session)],
    user_id: int = Depends(get_user_id)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user