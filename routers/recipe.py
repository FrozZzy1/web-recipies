from fastapi import APIRouter, Depends
from typing import Annotated

from models.recipe import Recipe
from repositories.recipe import RecipeRepository

recipe_router = APIRouter(
    prefix='/recipies',
    tags=['Рецепты'],
)


@recipe_router.post('')
async def create(recipe: Annotated[Recipe, Depends()]) -> dict:
    recipe_id = await RecipeRepository.create(recipe)
    return {'status': 'ok', 'recipe_id': recipe_id}


@recipe_router.get('')
async def get_all() -> dict:
    recipies = await RecipeRepository.get_all()
    return {'data': recipies}
