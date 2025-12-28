from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# Для ввода данных (регистрация)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=25)
    password_replay: str = Field(..., min_length=6, max_length=25)


# Для ввода данных (обновление)
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=25)


# Для ввода данных (смена пароля)
class UserChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=25)
    new_password_replay: str = Field(..., min_length=6, max_length=25)


# Для ответа API (без пароля)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    
    class Config:
        from_attributes = True  # для работы с SQLAlchemy моделями


# Для внутреннего использования (с паролем)
class UserInDB(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str
    
    class Config:
        from_attributes = True