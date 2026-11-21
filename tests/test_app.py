import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "healthy"}


def test_chat_success(client):
    res = client.post("/api/chat", json={"message": "How can I manage my monthly budget?"})
    assert res.status_code == 200
    assert res.get_json() == {"response": "You can start by tracking your income and expenses."}


def test_empty_message_rejection(client):
    res = client.post("/api/chat", json={"message": "   "})
    assert res.status_code == 400


def test_missing_message_rejection(client):
    res = client.post("/api/chat", json={"query": "hello"})
    assert res.status_code == 400


def test_invalid_json_handling(client):
    res = client.post("/api/chat", data="invalid-json", content_type="application/json")
    assert res.status_code == 400


def test_excessively_long_message(client):
    res = client.post("/api/chat", json={"message": "x" * 501})
    assert res.status_code == 400


def test_unexpected_input_type(client):
    res = client.post("/api/chat", json={"message": 999})
    assert res.status_code == 400