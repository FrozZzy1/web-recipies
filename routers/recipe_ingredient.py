from fastapi import APIRouter

from repositories.recipe_ingredient import RecipeIngredientRepository


recipe_ingredient_router = APIRouter(
    prefix='/recipe_ingredients',
    tags=['Ингредиенты для рецепта'],
)


@recipe_ingredient_router.post('')
async def create(
    recipe_id: int,
    ingredient_id: int,
    grams_amount: int,
):
    recipe_ingredient_id = await RecipeIngredientRepository.create(
        recipe_id, ingredient_id, grams_amount
    )
    return recipe_ingredient_id


@recipe_ingredient_router.get('')
async def get_all():
    recipe_ingredients = await RecipeIngredientRepository.get_all()
    return {'data': recipe_ingredients}
