import mock
from bmcook.core import Recipes
from bmcook.db import RecipeDB


def mock_get_recipes(cls, *args, **kwargs):
    return [{"name": "Mocked recipe name"}]


def mock_search_recipes_by_keywords(cls, *args, **kwargs):
    return [{"name": "Mocked and found recipe name"}]


def mock_get_recipe(cls, *args, **kwargs):
    return 1


def mock_add_recipe(cls, *args, **kwargs):
    return 1


def mock_delete_recipe(cls, *args, **kwargs):
    return 1


def mock_replace_recipe(cls, *args, **kwargs):
    return 1


def mock_update_recipe(cls, *args, **kwargs):
    return 1


def test_get_recipes():
    with mock.patch.object(RecipeDB, 'get_recipes', new=mock_get_recipes):
        recipes = Recipes().get_recipes()
        assert recipes[0]["name"] == "Mocked recipe name"
    with mock.patch.object(
            RecipeDB,
            'search_recipes_by_keywords',
            new=mock_search_recipes_by_keywords
    ):
        recipes = Recipes().get_recipes(search_words="a b c")
        assert recipes[0]["name"] == "Mocked and found recipe name"
