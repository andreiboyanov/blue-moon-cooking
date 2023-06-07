import pytest
import psycopg2
from fastapi.testclient import TestClient
from bmcook.main import app
from bmcook.db import config


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def fixture_init_db():
    connection = psycopg2.connect(
        database=config.db_name,
        user=config.db_user,
        password=config.db_password,
        host=config.db_host,
        port=config.db_port
    )
    cursor = connection.cursor()
    cursor.execute(open(r"bmcook/db/tools/init_db.sql", "r").read())
    cursor.execute(open(r"bmcook/tests/data/demo_data.sql", "r").read())
    connection.commit()
    cursor.close()
    connection.close()


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


def test_recipe_with_all_fields(test_client):
    result = test_client.post(
        "http://localhost:8000/recipes/",
        json={
            "name": "Test recipe",
            "description": "Test recipe with all fields filled in",
            "cooking_time": 999,
            "preparation": "Description of the preparation",
            "tags": ["tag1", "tag2", "meat"],
            "ingredients": [
                {"name": "meat", "quantity": 500, "unit": "g"},
                {"name": "onion", "quantity": 1, "unit": "pcs"},
                {"name": "product 1", "quantity": 999, "unit": "pcs"},
                {"name": "product 2", "quantity": None, "unit": None},
            ]
        }
    )
    assert result.status_code == 200
    result = test_client.get("http://localhost:8000/recipes/")
    assert result.status_code == 200
    recipes = result.json()
    last_recipe = recipes[-1]
    assert last_recipe["name"] == "Test recipe"
    assert last_recipe["description"] == "Test recipe with all fields filled in"
    assert last_recipe["cooking_time"] == 999
    assert last_recipe["preparation"] == "Description of the preparation"
    assert len(last_recipe["ingredients"]) == 4
    product_names = [product["name"] for product in last_recipe["ingredients"]]
    assert "meat" in product_names
    assert "onion" in product_names
    assert "product 1" in product_names
    assert "product 2" in product_names
    assert len(last_recipe["tags"]) == 3
    assert "tag1" in last_recipe["tags"]
    assert "tag2" in last_recipe["tags"]
    assert "meat" in last_recipe["tags"]
