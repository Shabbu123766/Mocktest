from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test GET
def test_get_students():
    response = client.get("/students")
    assert response.status_code == 200

# Test POST
def test_add_student():
    response = client.post("/students", json={
        "name": "Test",
        "age": 20,
        "course": "AI"
    })
    assert response.status_code == 200 or response.status_code == 201

from main import add_numbers

def test_add_numbers():
    assert add_numbers(2, 3) == 5

import pytest

@pytest.fixture
def sample_data():
    return {"a": 2, "b": 3}

def test_fixture(sample_data):
    assert sample_data["a"] + sample_data["b"] == 5