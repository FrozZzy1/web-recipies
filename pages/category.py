from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from routers.category import create, delete, get_all, update

router = APIRouter(
    prefix='/category_pages',
    tags=['Category pages']
)

templates = Jinja2Templates(directory='templates')


@router.post('/create')
async def create_category_template(
    request: Request,
):
    form = await request.form()
    name = form['name']
    await create(name)
    
    return RedirectResponse('/category_pages', status_code=303)


@router.get('')
async def get_categories_template(
    request: Request, categories=Depends(get_all)
):
    return templates.TemplateResponse(
        'categories.html',
        {
            'request': request,
            'categories': categories['data'],
        }
    )


@router.post('/delete/id={id}')
async def delete_category_template(request: Request, id: int):
    await delete(id)
    return RedirectResponse('/category_pages', status_code=303)


@router.post('/update/id={id}')
async def update_category_template(
    request: Request,
    id: int,
):
    form = await request.form()
    name = form['name']
    await update(id, name)
    return RedirectResponse('/category_pages', status_code=303)
