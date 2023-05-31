import pytest
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
