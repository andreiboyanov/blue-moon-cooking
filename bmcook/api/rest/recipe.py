from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

from .sample_data import RECIPES, get_fake_recipe

router = APIRouter()


class Recipe(BaseModel):
    id: int
    name: str
    description: str | None = None
    tags: list | None = None
    ingredients: list | None = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "ingredients": self.ingredients,
        }

@router.get("/")
def get_recipes(skip: int = 0, limit: int = 10):
    return RECIPES[skip:skip+limit]


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    recipe = get_fake_recipe(recipe_id)
    return recipe or Response(status_code=404)


@router.post("/")
def add_recipe(recipe: Recipe):
    existing_recipe = get_fake_recipe(recipe.id)
    if existing_recipe:
        return Response(status_code=409)
    RECIPES.append(recipe.to_dict())


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, recipe):
    return


@router.put("/recipe_id")
def replace_recipe(recipe_id: int, new_recipe):
    return


@router.patch("/recipe_id")
def modify_recipy(recipe_id: int, updates):
    return
