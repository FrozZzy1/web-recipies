from sqlalchemy.orm import Mapped, mapped_column

from orm.model import Model


class CategoryOrm(Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
