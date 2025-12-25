from typing import Annotated, AsyncGenerator
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from app.database.database import engine, Base, new_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

@app.post("/1")
async def ece(session: Annotated[AsyncSession, Depends(get_session)]):
    new_slug = Users(id=1, name="Vasya", email="inwdownd", hashed_password="kkkwwwii9823838")
    session.add(new_slug)
    await session.commit()