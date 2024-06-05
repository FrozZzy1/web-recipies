from fastapi import APIRouter, Depends
from typing import Annotated

from models.recipe_ingredient import RecipeIngredient
from repositories.recipe_ingredient import RecipeIngredientRepository


recipe_ingredient_router = APIRouter(
    prefix='/recipe_ingredients',
    tags=['Ингредиенты для рецепта'],
)


@recipe_ingredient_router.post('')
async def create(
    recipe_ingredient: Annotated[RecipeIngredient, Depends()]
):
    recipe_ingredient_id = await RecipeIngredientRepository.create(
        recipe_ingredient
    )
    return recipe_ingredient_id


@recipe_ingredient_router.get('')
async def get_all():
    recipe_ingredients = await RecipeIngredientRepository.get_all()
    return {'data': recipe_ingredients}
