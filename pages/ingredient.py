from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from routers.ingredient import get_all, delete, update, create

from fastapi import APIRouter

router = APIRouter(
    prefix='/ingredient_pages',
    tags=['Ingredient pages']
)

templates = Jinja2Templates(directory='templates')


@router.post('/create')
async def create_ingredient_template(
    request: Request,
):
    form = await request.form()
    name = form['name']
    await create(name)
    return templates.TemplateResponse(
        'ingredients.html',
        {
            'request': request,
        }
    )


@router.get('')
async def get_ingredients_template(
    request: Request, ingredients=Depends(get_all)
):
    return templates.TemplateResponse(
        'ingredients.html',
        {
            'request': request,
            'ingredients': ingredients['data'],
        }
    )


@router.post('/delete/id={id}')
async def delete_ingredient_template(request: Request, id: int):
    await delete(id)
    return templates.TemplateResponse(
        'ingredients.html',
        {
            'request': request,
        }
    )


@router.post('/update/id={id}')
async def update_ingredient_template(
    request: Request,
    id: int,
):
    form = await request.form()
    name = form['name']
    await update(id, name)
    return templates.TemplateResponse(
        'ingredients.html',
        {
            'request': request,
        }
    )
