from sqlalchemy import select

from database.database import session
from models.category import Category
from orm.category import CategoryOrm


class CategoryRepository:
    @classmethod
    async def create(cls, data: Category) -> None:
        async with session() as current_session:
            category_dict = data.model_dump()
            category = CategoryOrm(**category_dict)
            current_session.add(category)
            await current_session.commit()
            return category.id

    @classmethod
    async def get_all(cls) -> Category:
        async with session() as current_session:
            query = select(CategoryOrm)
            result = await current_session.execute(query)
            category_models = result.scalars().all()
            return category_models
