from fastapi import APIRouter

from repositories.recipe import RecipeRepository

recipe_router = APIRouter(
    prefix='/recipies',
    tags=['Рецепты'],
)


@recipe_router.post('')
async def create(
    name: str,
    category_id: int,
    rating: int,
) -> dict:
    recipe_id = await RecipeRepository.create(name, category_id, rating)
    return {'status': 'ok', 'recipe_id': recipe_id}


@recipe_router.get('')
async def get_all() -> dict:
    recipies = await RecipeRepository.get_all()
    return {'data': recipies}


@recipe_router.get('')
async def get_by_id(id: int) -> dict:
    recipe, ingredients_list = await RecipeRepository.get_by_id(id)
    return {'data': recipe, 'ingredients': ingredients_list}


@recipe_router.delete('/id={id}')
async def delete(id: int):
    await RecipeRepository.delete_by_id(id)

    return {"message": "Ingredient deleted succesfully"}


@recipe_router.put('')
async def update(
    id: int,
    name: str,
    category_id: int,
    rating: int
):
    recipe = await RecipeRepository.update_by_id(
        id, name, category_id, rating
    )

    return {'new_recipe': recipe}
