from contextlib import suppress

import sqlalchemy
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from database.database import session
from models.recipe import Recipe
from orm.ingredient import IngredientOrm
from orm.recipe import RecipeOrm
from orm.recipe_ingredient import RecipeIngredientOrm


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
            ingredients_query = await current_session.execute(
                select(IngredientOrm.id, IngredientOrm.name, RecipeIngredientOrm.grams_amount)
                .join(RecipeIngredientOrm,
                      IngredientOrm.id == RecipeIngredientOrm.ingredient_id)
                .filter(RecipeIngredientOrm.recipe_id == id)
            )
            ingredients = ingredients_query.all()

            ingredients_list = [{
                'id': ingredient[0],
                'name': ingredient[1],
                'grams': ingredient[2]
                }
                                for ingredient in ingredients]

            result = await current_session.execute(query)
            result_orm: RecipeOrm = result.scalar()

            return result_orm, ingredients_list

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
            recipe, _ = await cls.get_by_id(id)
            recipe.name = name
            recipe.category_id = category_id
            recipe.rating = rating
            current_session.add(recipe)
            await current_session.commit()

            return recipe
