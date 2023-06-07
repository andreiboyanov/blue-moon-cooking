from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bmcook.core import Recipes
from bmcook.exceptions import RecipeDataError


router = APIRouter()


class Ingredient(BaseModel):
    id: int | None = None
    name: str
    quantity: int | None = None
    unit: str | None = None


class Recipe(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    cooking_time: int | None = None
    preparation: str | None = None
    tags: List[str] = []
    ingredients: List[Ingredient] = []


@router.get("/")
async def get_recipes(skip: int = 0, limit: int = 10):
    return Recipes().get_recipes(skip, limit) or []


@router.get("/{recipe_id}")
async def get_recipe(recipe_id: int):
    recipe = Recipes().get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404)
    return recipe


@router.post("/")
async def add_recipe(recipe: Recipe):
    try:
        Recipes().add_recipe(recipe.dict())
    except RecipeDataError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: int):
    Recipes().delete_recipe(recipe_id)


@router.put("/{recipe_id}")
async def replace_recipe(recipe_id: int, new_recipe: Recipe):
    try:
        result = Recipes().replace_recipe(recipe_id, new_recipe.dict())
    except RecipeDataError as error:
        raise HTTPException(status_code=409, detail=str(error))
    if result is False:
        raise HTTPException(status_code=404)


@router.patch("/{recipe_id}")
async def modify_recipy(recipe_id: int, updates: dict):
    try:
        result = Recipes().update_recipe(recipe_id, updates)
    except RecipeDataError as error:
        raise HTTPException(status_code=409, detail=str(error))
    if result is False:
        raise HTTPException(status_code=404)
