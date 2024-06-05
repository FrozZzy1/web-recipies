from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from orm.model import Model
from orm.category import CategoryOrm
if TYPE_CHECKING:
    from orm.ingredient import IngredientOrm


class RecipeOrm(Model):
    __tablename__ = 'recipies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped[CategoryOrm] = relationship()
    rating: Mapped[int]
    ingredients: Mapped[list['IngredientOrm']] = relationship(
        secondary='recipe_ingredients',
        backref='ingredients',
    )
