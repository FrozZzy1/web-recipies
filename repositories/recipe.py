import sqlalchemy
from contextlib import suppress
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from models.recipe import Recipe
from database.database import session
from orm.recipe import RecipeOrm


class RecipeRepository:
    @classmethod
    async def create(
        cls,
        name: str,
        category_id: int,
        rating: int,
    ):
        with suppress(sqlalchemy.exc.IntegrityError):
            async with session() as current_session:
                recipe = RecipeOrm(
                    name=name,
                    category_id=category_id,
                    rating=rating,
                )
                current_session.add(recipe)
                await current_session.commit()
                return recipe.id

    @classmethod
    async def get_all(cls):
        async with session() as current_session:
            query = (
                select(RecipeOrm)
                .options(joinedload(RecipeOrm.category))
                )
            result = await current_session.execute(query)
            result_orm = result.scalars().all()
            result_dto = [Recipe.model_validate(row, from_attributes=True)
                          for row in result_orm]
            return result_dto

    @classmethod
    async def get_by_id(cls, id: int):
        async with session() as current_session:
            query = (
                select(RecipeOrm)
                .where(RecipeOrm.id == id)
            )
            result = await current_session.execute(query)
            result_orm = result.scalar()

            return result_orm
        
    @classmethod
    async def delete_by_id(cls, id: int):
        async with session() as current_session:
            query = delete(RecipeOrm).where(RecipeOrm.id == id)
            await current_session.execute(query)
            await current_session.commit()

    @classmethod
    async def update_by_id(
        cls,
        id: int,
        name: str,
        category_id: int,
        rating: int,
    ):
        async with session() as current_session:
            recipe = await cls.get_by_id(id)
            recipe.name = name
            recipe.category_id = category_id
            recipe.rating = rating
            current_session.add(recipe)
            await current_session.commit()

            return recipe
