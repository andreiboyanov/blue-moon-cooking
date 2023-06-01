from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

from .sample_data import (
    fake_recipes, get_fake_recipe, delete_fake_recipe, replace_fake_recipe
)

router = APIRouter()


class Recipe(BaseModel):
    id: int
    name: str
    description: str | None = None
    tags: list | None = None
    ingredients: list | None = None


@router.get("/")
def get_recipes(skip: int = 0, limit: int = 10):
    return fake_recipes[skip:skip + limit]


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    recipe = get_fake_recipe(recipe_id)
    return recipe or Response(status_code=404)


@router.post("/")
def add_recipe(recipe: Recipe):
    existing_recipe = get_fake_recipe(recipe.id)
    if existing_recipe:
        return Response(status_code=409)
    fake_recipes.append(recipe.dict())


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int):
    delete_fake_recipe(recipe_id)


@router.put("/{recipe_id}")
def replace_recipe(recipe_id: int, new_recipe: Recipe):
    if recipe_id != new_recipe.id:
        return Response(status_code=422)
    result = replace_fake_recipe(recipe_id, new_recipe.dict())
    if result is False:
        return Response(status_code=404)


@router.patch("/{recipe_id}")
def modify_recipy(recipe_id: int, updates: dict):
    recipe = get_fake_recipe(recipe_id)
    if not recipe:
        return Response(status_code=404)
    for key, value in updates.items():
        if key == "id":
            continue
        if key in recipe:
            recipe[key] = value
