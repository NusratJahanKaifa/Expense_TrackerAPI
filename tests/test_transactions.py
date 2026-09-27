from datetime import date

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def get_token():
    username = "testuser"
    password = "test12345"

    register_data = {
        "username": username,
        "email": "test@example.com",
        "password": password
    }

    client.post("/auth/register", json=register_data)

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    return login_response.json()["access_token"]


def create_test_transaction(token):
    response = client.post(
        "/transactions",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Test Food",
            "amount": 500,
            "type": "expense",
            "category": "Food",
            "date": str(date.today())
        }
    )

    return response


def test_get_transactions():
    token = get_token()

    response = client.get(
        "/transactions",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_get_specific_transaction():
    token = get_token()

    transaction_response = create_test_transaction(token)
    transaction_id = transaction_response.json()["id"]

    response = client.get(
        f"/transactions/{transaction_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == transaction_id


def test_create_transaction():
    token = get_token()

    response = create_test_transaction(token)

    assert response.status_code == 201
    assert response.json()["title"] == "Test Food"


def test_update_transaction():
    token = get_token()

    transaction_response = create_test_transaction(token)
    transaction_id = transaction_response.json()["id"]

    response = client.put(
        f"/transactions/{transaction_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Updated Food",
            "amount": 700,
            "type": "expense",
            "category": "Food",
            "date": str(date.today())
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Food"


def test_delete_transaction():
    token = get_token()

    transaction_response = create_test_transaction(token)
    transaction_id = transaction_response.json()["id"]

    response = client.delete(
        f"/transactions/{transaction_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200