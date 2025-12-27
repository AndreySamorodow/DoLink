from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],  # argon2 основной, bcrypt запасной
    deprecated="auto"
)

def get_password_hash(password: str) -> str:  # ← убрал async!
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def verify_user_reg_data(db, user_data: UserCreate):
        query = select(User).filter_by(email=user_data.email)
        result = await db.execute(query)
        verify_email = result.scalar_one_or_none()
        if verify_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email address already exists")
        if user_data.password != user_data.password_replay:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password repetition")
