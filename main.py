from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.database import create_tables

from routers.category import category_router
from routers.ingredient import ingredient_router
from routers.recipe import recipe_router
from routers.recipe_ingredient import recipe_ingredient_router

from pages.ingredient import router as ingredient_pages_router
from pages.category import router as category_pages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    await create_tables()
    yield


app = FastAPI(
    title='рецепты',
    lifespan=lifespan,
)

app.include_router(category_router)
app.include_router(ingredient_router)
app.include_router(recipe_router)
app.include_router(recipe_ingredient_router)
app.include_router(ingredient_pages_router)
app.include_router(category_pages_router)
