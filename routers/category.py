from fastapi import APIRouter

from repositories.category import CategoryRepository

category_router = APIRouter(
    prefix='/categories',
    tags=['Категории'],
)


@category_router.post('')
async def create(
    name: str
) -> dict:
    category_id = await CategoryRepository.create(name)
    return {'status': 'ok', 'category_id': category_id}


@category_router.get('')
async def get_all() -> dict:
    categories = await CategoryRepository.get_all()
    return {'data': categories}


@category_router.get('/id={id}')
async def get_by_id(id: int):
    category = await CategoryRepository.get_by_id(id)
    return {'category': category}


@category_router.delete('/id={id}')
async def delete(id: int):
    await CategoryRepository.delete_by_id(id)

    return {"message": "Category deleted succesfully"}


@category_router.put('')
async def update(
    id: int,
    name: str,
):
    category = await CategoryRepository.update_by_id(
        id, name
    )

    return {'new_category': category}
