from sqlalchemy.orm import Mapped, mapped_column

from orm.model import Model


class IngredientOrm(Model):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
