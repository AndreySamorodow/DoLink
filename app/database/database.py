from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)
new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

#for use --> session: Annotated[AsyncSession, Depends(get_session)]
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
