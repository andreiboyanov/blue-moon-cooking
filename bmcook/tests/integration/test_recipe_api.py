import pytest
from fastapi.testclient import TestClient
from bmcook.main import app


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)


def test_get_recipes(test_client):
    result = test_client.get("http://localhost:8000/recipes/")
    from pprint import pprint
    pprint(result.json())
    assert len(result.json()) == 2
