from typing import Annotated
from fastapi import APIRouter, Depends

from models.category import Category
from repositories.category import CategoryRepository

category_router = APIRouter(
    prefix='/categories',
)


@category_router.post('')
async def create(
    category: Annotated[Category, Depends()],
):
    category_id = await CategoryRepository.create(category)
    return {'status': 'ok', 'category_id': category_id}


@category_router.get('')
async def get_all():
    categories = await CategoryRepository.get_all()
    return {'data': categories}
