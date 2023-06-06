from bmcook.db import RecipeDB, RecipeType
from typing import List


class Recipes:
    def __init__(self):
        pass
    def get_recipes(
        self, skip: int = 0, limit: int = 10,
        search_words: str or None = None
    ) -> List[RecipeType] or None:
        with RecipeDB() as db:
            if search_words is None:
                return db.get_recipes(skip, limit)
            else:
                return db.search_recipes_by_keywords(search_words, skip, limit)

    def get_recipe(self, recipe_id: int) -> RecipeType or None:
        with RecipeDB() as db:
            return db.get_recipe(recipe_id)

    def add_recipe(self, recipe: RecipeType) -> None:
        with RecipeDB() as db:
            return db.add_recipe(recipe)

    def delete_recipe(self, recipe_id: int) -> None:
        with RecipeDB() as db:
            db.delete_recipe(recipe_id)

    def replace_recipe(self, recipe_id: int, new_recipe: RecipeType) -> bool:
        with RecipeDB() as db:
            if db.get_recipe(recipe_id) is None:
                return False
            db.replace_recipe(recipe_id, new_recipe)
            return True

    def update_recipe(self, recipe_id: int, updates: RecipeType) -> bool:
        with RecipeDB() as db:
            if db.get_recipe(recipe_id) is None:
                return False
            db.update_recipe(recipe_id, updates)
