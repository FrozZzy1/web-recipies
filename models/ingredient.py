from pydantic import BaseModel


class Ingredient(BaseModel):
    id: int | None = None
    name: str
