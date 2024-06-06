from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from routers.category import get_all as get_all_categories
from routers.category import get_by_id as get_category_by_id
from routers.recipe import create, delete, get_all, get_by_id, update

router = APIRouter(
    prefix='/recipe_pages',
    tags=['Recipes pages']
)

templates = Jinja2Templates(directory='templates')


@router.post('/create')
async def create_recipe_template(
    request: Request,
):
    form = await request.form()
    name = form['name']
    category_id = int(form['category'])
    rating = int(form['rating'])
    await create(name, category_id, rating)

    return RedirectResponse('/recipe_pages', status_code=303)


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
    
    return RedirectResponse('/recipe_pages', status_code=303)


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

    return RedirectResponse('/recipe_pages', status_code=303)


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
            'ingredients': recipe['ingredients'],
        }
    )
