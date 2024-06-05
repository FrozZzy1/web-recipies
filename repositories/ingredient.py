from contextlib import suppress
import sqlalchemy

from sqlalchemy import delete, select

from models.ingredient import Ingredient
from database.database import session
from orm.ingredient import IngredientOrm


class IngredientRepository:
    # @classmethod
    # async def create(cls, data: Ingredient):
    #     with suppress(sqlalchemy.exc.IntegrityError):
    #         async with session() as current_session:
    #             ingredient = IngredientOrm(
    #                 name=data.name,
    #             )
    #             current_session.add(ingredient)
    #             await current_session.commit()
    #             return ingredient.id

    @classmethod
    async def create(cls, name: str):
        with suppress(sqlalchemy.exc.IntegrityError):
            async with session() as current_session:
                ingredient = IngredientOrm(
                    name=name,
                )
                current_session.add(ingredient)
                await current_session.commit()
                
                return {'data': ingredient}
    
    @classmethod
    async def get_all(cls):
        async with session() as current_session:
            query = (
                select(IngredientOrm)
            )
            result = await current_session.execute(query)
            result_orm = result.scalars().all()
            result_dto = [Ingredient.model_validate(row, from_attributes=True)
                          for row in result_orm]
            return result_dto

    @classmethod
    async def get_by_id(cls, id: int):
        async with session() as current_session:
            query = (
                select(IngredientOrm)
                .where(IngredientOrm.id == id)
            )
            result = await current_session.execute(query)
            result_orm = result.scalars().first()

            return result_orm

    @classmethod
    async def delete_by_id(cls, id: int):
        async with session() as current_session:
            query = delete(IngredientOrm).where(IngredientOrm.id == id)
            await current_session.execute(query)
            await current_session.commit()

    @classmethod
    async def update_by_id(cls, id: int, name: str):
        async with session() as current_session:
            ingredient = await cls.get_by_id(id)
            ingredient.name = name
            current_session.add(ingredient)
            await current_session.commit()

            return ingredient
