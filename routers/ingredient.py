from fastapi import APIRouter

from repositories.ingredient import IngredientRepository

ingredient_router = APIRouter(
    prefix='/ingredients',
    tags=['Ингредиенты'],
)


@ingredient_router.post('')
async def create(
    name: str
) -> dict:
    ingredient_id = await IngredientRepository.create(name)
    return {'status': 'ok', 'ingredient_id': ingredient_id}


@ingredient_router.get('')
async def get_all() -> dict:
    ingredients = await IngredientRepository.get_all()
    return {'data': ingredients}


@ingredient_router.get('/id={id}')
async def get_by_id(id: int):
    ingredient = await IngredientRepository.get_by_id(id)
    return {'ingredient': ingredient}


@ingredient_router.delete('/id={id}')
async def delete(id: int):
    await IngredientRepository.delete_by_id(id)

    return {"message": "Ingredient deleted succesfully"}


@ingredient_router.put('')
async def update(
    id: int,
    name: str,
):
    ingredient = await IngredientRepository.update_by_id(
        id, name
    )

    return {'new_ingredient': ingredient}
