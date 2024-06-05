from pydantic import BaseModel

from models.ingredient import Ingredient
from models.recipe import Recipe


class RecipeIngredient(BaseModel):
    recipe_id: int
    recipe: Recipe | None = None
    ingredient_id: int
    ingredient: Ingredient | None = None
    grams_amount: int
