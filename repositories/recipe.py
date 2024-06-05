import sqlalchemy
from contextlib import suppress
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.recipe import Recipe
from database.database import session
from orm.recipe import RecipeOrm


class RecipeRepository:
    @classmethod
    async def create(cls, data: Recipe):
        with suppress(sqlalchemy.exc.IntegrityError):
            async with session() as current_session:
                recipe = RecipeOrm(
                    name=data.name,
                    category_id=data.category_id,
                    rating=data.rating,
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
