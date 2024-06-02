from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model import Model
from orm.category import CategoryOrm


class RecipeOrm(Model):
    __tablename__ = 'recipies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category_id: Mapped[int] = ForeignKey('categories.id')
    category: Mapped[CategoryOrm] = relationship()
    rating: Mapped[int]
