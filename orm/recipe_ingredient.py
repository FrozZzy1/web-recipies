from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from orm.model import Model


class RecipeIngredientOrm(Model):
    __tablename__ = 'recipe_ingredients'

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey('recipies.id'),
        primary_key=True,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey('ingredients.id'),
        primary_key=True
    )
    grams_amount: Mapped[int]
