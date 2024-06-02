from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Model
from orm.ingredient import IngredientOrm
from recipe import RecipeOrm


class RecipeIngredientOrm(Model):
    __tablename__ = 'recipe_ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipies.id'))
    recipe: Mapped[RecipeOrm] = relationship()
    ingredient_id: Mapped[int] = mapped_column(ForeignKey('ingredients.id'))
    ingredient: Mapped[IngredientOrm] = relationship()
    grams_amount: Mapped[int]
