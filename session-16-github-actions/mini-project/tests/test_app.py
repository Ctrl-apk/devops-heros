import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "Hello World" in data["message"]


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_add(client):
    response = client.get("/add/3/5")
    assert response.status_code == 200
    assert response.get_json()["result"] == 8


def test_subtract(client):
    response = client.get("/subtract/10/4")
    assert response.status_code == 200
    assert response.get_json()["result"] == 6


def test_multiply(client):
    response = client.get("/multiply/4/5")
    assert response.status_code == 200
    assert response.get_json()["result"] == 20


def test_divide(client):
    response = client.get("/divide/10/2")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5.0


def test_divide_by_zero(client):
    response = client.get("/divide/10/0")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "zero" in data["error"].lower()
