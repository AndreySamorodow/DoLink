from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers import tasks_router

from app.database.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)

from app.test_create_db.create import create_db_router
app.include_router(create_db_router)
