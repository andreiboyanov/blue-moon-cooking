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
    result = test_client.get("http://localhost:8000/recipes/?skip=1&limit=1")
    assert result.json()[0]["id"] == 2


def test_get_recipe(test_client):
    result = test_client.get("http://localhost:8000/recipes/1")
    assert result.json()["id"] == 1


def test_get_recipe_non_existent(test_client):
    result = test_client.get("http://localhost:8000/recipes/3")
    assert result.status_code == 404


def test_create_recipe(test_client):
    result = test_client.post("http://localhost:8000/recipes/", data={"id": 3})
    assert result.status_code == 200
    result = test_client.get("http://localhost:8000/recipes/3")
    assert result.status_code == 200
