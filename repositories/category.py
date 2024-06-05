from contextlib import suppress
import sqlalchemy

from sqlalchemy import delete, select

from models.category import Category
from database.database import session
from orm.category import CategoryOrm


class CategoryRepository:
    @classmethod
    async def create(cls, name: str):
        with suppress(sqlalchemy.exc.IntegrityError):
            async with session() as current_session:
                category = CategoryOrm(
                    name=name,
                )
                current_session.add(category)
                await current_session.commit()
                
                return {'data': category}
    
    @classmethod
    async def get_all(cls):
        async with session() as current_session:
            query = (
                select(CategoryOrm)
            )
            result = await current_session.execute(query)
            result_orm = result.scalars().all()
            result_dto = [Category.model_validate(row, from_attributes=True)
                          for row in result_orm]
            return result_dto

    @classmethod
    async def get_by_id(cls, id: int):
        async with session() as current_session:
            query = (
                select(CategoryOrm)
                .where(CategoryOrm.id == id)
            )
            result = await current_session.execute(query)
            result_orm = result.scalars().first()

            return result_orm

    @classmethod
    async def get_id_by_name(cls, name: str):
        async with session() as current_session:
            query = (
                select(CategoryOrm)
                .where(CategoryOrm.name == name)
            )
            result = await current_session.execute(query)
            result_orm = result.scalars().first()
            return result_orm.id

    @classmethod
    async def delete_by_id(cls, id: int):
        async with session() as current_session:
            query = delete(CategoryOrm).where(CategoryOrm.id == id)
            await current_session.execute(query)
            await current_session.commit()

    @classmethod
    async def update_by_id(cls, id: int, name: str):
        async with session() as current_session:
            category = await cls.get_by_id(id)
            category.name = name
            current_session.add(category)
            await current_session.commit()

            return category
