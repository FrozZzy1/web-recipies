from pydantic import BaseModel

from models.category import Category
from models.ingredient import Ingredient


class Recipe(BaseModel):
    id: int | None = None
    name: str
    category_id: int
    category: Category | None = None
    rating: int
    ingredients: list[Ingredient] | None = None
