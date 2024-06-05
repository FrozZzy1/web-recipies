from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from routers.recipe import get_all, create, delete, update, get_by_id
from routers.category import get_all as get_all_categories
from routers.category import get_by_id as get_category_by_id

from fastapi import APIRouter

router = APIRouter(
    prefix='/recipes_pages',
    tags=['Recipes pages']
)

templates = Jinja2Templates(directory='templates')


@router.post('/create')
async def create_recipe_template(
    request: Request,
):
    form = await request.form()
    print(form)
    name = form['name']
    category_id = int(form['category'])
    rating = int(form['rating'])
    await create(name, category_id, rating)
    return templates.TemplateResponse(
        'recipes.html',
        {
            'request': request,
        }
    )


@router.get('')
async def get_recipe_template(
    request: Request, recipes=Depends(get_all)
):
    categories = await get_all_categories()

    return templates.TemplateResponse(
        'recipes.html',
        {
            'request': request,
            'recipes': recipes['data'],
            'categories': categories['data'],
        }
    )


@router.post('/delete/id={id}')
async def delete_recipe_template(request: Request, id: int):
    await delete(id)
    return templates.TemplateResponse(
        'recipes.html',
        {
            'request': request,
        }
    )


@router.post('/update/id={id}')
async def update_recipe_template(
    request: Request,
    id: int,
):
    form = await request.form()
    name = form['name']
    category_id = int(form['category'])
    rating = int(form['rating'])
    await update(id, name, category_id, rating)
    return templates.TemplateResponse(
        'recipes.html',
        {
            'request': request,
        }
    )


@router.get('/recipe/{id}')
async def get_recipe(
    request: Request,
    id: int,
):
    recipe = await get_by_id(id)
    recipe['data'].category = await get_category_by_id(
        recipe['data'].category_id
    )
    return templates.TemplateResponse(
        'recipe.html',
        {
            'request': request,
            'recipe': recipe['data'],
        }
    )
