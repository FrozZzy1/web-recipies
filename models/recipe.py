from pydantic import BaseModel

from models.category import Category


class Recipe(BaseModel):
    name: str
    category: Category
    rating: int
