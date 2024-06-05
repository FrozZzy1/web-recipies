from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from routers.category import get_all, delete, update, create

from fastapi import APIRouter

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
    return templates.TemplateResponse(
        'categories.html',
        {
            'request': request,
        }
    )


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
    return templates.TemplateResponse(
        'categories.html',
        {
            'request': request,
        }
    )


@router.post('/update/id={id}')
async def update_category_template(
    request: Request,
    id: int,
):
    form = await request.form()
    name = form['name']
    await update(id, name)
    return templates.TemplateResponse(
        'categories.html',
        {
            'request': request,
        }
    )
