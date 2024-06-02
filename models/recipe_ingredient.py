from pydantic import BaseModel

from models.ingredient import Ingredient
from recipe import Recipe


class RecipeIngredient(BaseModel):
    recipe: Recipe
    ingredient: Ingredient
    grams_amount: int
