import sqlalchemy

from contextlib import suppress
from sqlalchemy import select

from models.recipe_ingredient import RecipeIngredient
from database.database import session
from orm.ingredient import IngredientOrm
from orm.recipe import RecipeOrm
from orm.recipe_ingredient import RecipeIngredientOrm


class RecipeIngredientRepository:
    @classmethod
    async def create(cls, data: RecipeIngredient):
        with suppress(sqlalchemy.exc.IntegrityError):
            async with session() as current_session:
                recipe_ingredient = RecipeIngredientOrm(
                    recipe_id=data.recipe_id,
                    ingredient_id=data.ingredient_id,
                    grams_amount=data.grams_amount,
                )
                current_session.add(recipe_ingredient)
                await current_session.commit()
                return {'status': 'ok'}

    @classmethod
    async def get_all(cls):
        async with session() as current_session:
            query = (
                select(RecipeIngredientOrm)
                # .options(selectinload(RecipeIngredientOrm.recipe))
                # .options(selectinload(RecipeIngredientOrm.ingredients))
            )
            result = await current_session.execute(query)
            result_orm = result.scalars().all()
            result_dto = [RecipeIngredient.model_validate(row,
                                                          from_attributes=True)
                          for row in result_orm]
            return result_dto

    @classmethod
    async def get_all_ingredients_by_recipe(cls, recipe_id: int):
        async with session() as current_session:
            ingredients_by_grams = current_session.query(
                IngredientOrm, RecipeIngredientOrm.grams_amount).join(
                    RecipeIngredientOrm,
                    (IngredientOrm.id == RecipeIngredientOrm.ingredient_id) and
                    (RecipeOrm.id == RecipeIngredientOrm.recipe_id),
                    isouter=True
                ).filter(RecipeIngredientOrm.recipe_id == recipe_id).all()

            ingredients_by_recipe = {}
            for ingredient, grams in ingredients_by_grams:
                ingredients_by_recipe[ingredient.name] = grams

            return ingredients_by_recipe
