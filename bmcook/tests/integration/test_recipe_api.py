import pytest
import json
from fastapi.testclient import TestClient
from bmcook.main import app


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)


def test_get_recipes(test_client):
    result = test_client.get("http://localhost:8000/recipes/")
    assert len(result.json()) == 2


def test_get_recipes_with_limit_1(test_client):
    result = test_client.get("http://localhost:8000/recipes/?limit=1")
    assert len(result.json()) == 1


def test_get_recipes_starting_from_the_second(test_client):
    all_recipes = test_client.get("http://localhost:8000/recipes/").json()
    one_recipe = \
        test_client.get("http://localhost:8000/recipes/?skip=1&limit=1").json()[
            0]
    assert one_recipe["id"] == all_recipes[1]["id"]


def test_get_recipe(test_client):
    result = test_client.get("http://localhost:8000/recipes/1")
    assert result.json()["id"] == 1


def test_get_recipe_non_existent(test_client):
    result = test_client.get("http://localhost:8000/recipes/9999999")
    assert result.status_code == 404


def test_create_recipe(test_client):
    old_recipe_count = len(
        test_client.get("http://localhost:8000/recipes/").json()
    )
    result = test_client.post(
        "http://localhost:8000/recipes/",
        json={"id": 3, "name": "Some new recipe"}
    )
    assert result.status_code == 200
    recipes = test_client.get("http://localhost:8000/recipes/").json()
    new_recipe_count = len(recipes)
    assert new_recipe_count == old_recipe_count + 1
    last_recipe = recipes[-1]
    assert last_recipe["id"] == 3
    assert last_recipe["name"] == "Some new recipe"


def test_create_recipe_with_existing_id(test_client):
    result = test_client.post(
        "http://localhost:8000/recipes/",
        json={"id": 2, "name": "Some new recipe"}
    )
    assert result.status_code == 409


def test_delete_recipe(test_client):
    result = test_client.delete("http://localhost:8000/recipes/2")
    assert result.status_code == 200
    result = test_client.get("http://localhost:8000/recipes/2")
    assert result.status_code == 404


def test_update_recipe(test_client):
    all_recipes = test_client.get("http://localhost:8000/recipes/").json()
    update_id = all_recipes[0]["id"]
    result = test_client.put(
        f"http://localhost:8000/recipes/{update_id}",
        json={
            "id": update_id,
            "name": "Some new recipe name for test_update_recipe"
        }
    )
    assert result.status_code == 200
    result = test_client.get(f"http://localhost:8000/recipes/{update_id}")
    assert result.status_code == 200
    assert result.json()[
               "name"
           ] == "Some new recipe name for test_update_recipe"


def test_update_recipe_non_existing(test_client):
    result = test_client.put(
        "http://localhost:8000/recipes/99",
        json={"id": 99, "name": "Some new recipe name"}
    )
    assert result.status_code == 404


def test_update_recipe_with_wrong_id(test_client):
    result = test_client.put(
        "http://localhost:8000/recipes/1",
        json={"id": 99, "name": "Some new recipe name"}
    )
    assert result.status_code == 422


def test_patch_recipe(test_client):
    result = test_client.patch(
        "http://localhost:8000/recipes/1",
        json={"id": 99, "description": "Some new recipe description"}
    )
    assert result.status_code == 200
    result = test_client.get("http://localhost:8000/recipes/1")
    assert result.status_code == 200
    assert result.json()["description"] == "Some new recipe description"
    assert result.json()["id"] == 1


def test_patch_recipe_non_existent(test_client):
    result = test_client.patch(
        "http://localhost:8000/recipes/99",
        json={"id": 99, "description": "Some new recipe description"}
    )
    assert result.status_code == 404
