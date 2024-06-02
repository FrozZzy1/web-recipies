from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.database import create_tables, delete_tables
from routers.category import category_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(
    title='рецепты',
    lifespan=lifespan,
)

app.include_router(category_router)
