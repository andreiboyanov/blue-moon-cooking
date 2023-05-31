from fastapi import APIRouter
from fastapi.responses import Response

from .sample_data import RECIPES

router = APIRouter()


@router.get("/")
def get_recipes(skip: int = 0, limit: int = 10):
    result = RECIPES.copy()
    result.append({"skip": skip, "limit": limit})
    return result


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    for recipe in RECIPES:
        if recipe["id"] == recipe_id:
            return recipe
    return Response(status_code=404)


@router.post("/")
def add_recipe():
    return


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, recipe):
    return


@router.put("/recipe_id")
def replace_recipe(recipe_id: int, new_recipe):
    return


@router.patch("/recipe_id")
def modify_recipy(recipe_id: int, updates):
    return
