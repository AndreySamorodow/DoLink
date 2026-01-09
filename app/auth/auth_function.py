from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserLogin
from app.database.dao import UserDao
from app.config import settings

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


def get_token(request: Request):
    token = request.cookies.get("LinkDo_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def verify_user_reg_data(db: AsyncSession, user_data: UserCreate):
    verify_email = await UserDao.find_one_or_none(db, email=user_data.email)

    if verify_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email address already exists")
    if user_data.password != user_data.password_replay:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password repetition")


async def verify_user_log_data(db: AsyncSession, user_data: UserLogin):
    user = await UserDao.find_one_or_none(db, email=user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="False data")
    return user


async def get_user_id(token = Depends(get_token)):
    try:
        payload = jwt.decode(
        token, settings.SECRET_KEY, settings.ALGORITHM
    )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
    return int(user_id)