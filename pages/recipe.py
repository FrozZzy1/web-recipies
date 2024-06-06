from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from routers.category import get_all as get_all_categories
from routers.category import get_by_id as get_category_by_id
from routers.recipe import create, delete, get_all, get_by_id, update
from routers.recipe_ingredient import create as create_recipe_ingredient
from repositories.ingredient import IngredientRepository

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


@router.post('/recipe_ingredient/recipe_id={recipe_id}')
async def create_recipe_ingredient_template(
    request: Request,
    recipe_id: int,
):
    form = await request.form()
    
    if not form.get('ingredient'):
        return RedirectResponse(f'/recipe_pages/recipe/{recipe_id}', status_code=303)
    
    ingredient_id = int(form['ingredient'])
    grams_amount = int(form['grams_amount'])
    await create_recipe_ingredient(
        recipe_id, ingredient_id, grams_amount
    )
    
    return RedirectResponse(f'/recipe_pages/recipe/{recipe_id}',
                            status_code=303)


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
    ingredients_for_recipe_id = [
        ingredient['id'] for ingredient in recipe['ingredients']
    ]
    all_ingredients_id = [
        ingredient.id for ingredient in await IngredientRepository.get_all()
    ]
    ingredients_id = [
        id for id in all_ingredients_id if id not in ingredients_for_recipe_id
    ]
    ingredients = [
        await IngredientRepository.get_by_id(id) for id in ingredients_id
    ]


    return templates.TemplateResponse(
        'recipe.html',
        {
            'request': request,
            'recipe': recipe['data'],
            'ingredients': recipe['ingredients'],
            'list_ingredients': ingredients,
        }
    )
