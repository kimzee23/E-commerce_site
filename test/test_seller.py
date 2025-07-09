import json
from unittest.mock import patch



def test_seller_register_is_successful(test_client):
    payload = {
        "name": "amidat bread",
        "email": "amidat@gmail.com",
        "password": "password",
        "phone": "08123456781",
        "role": "seller"
    }

    with patch("app.routes.seller_controller.mail.send"):
        response = test_client.post(
            "/api/sellers/register",
            data=json.dumps(payload),
            content_type="application/json"
        )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Seller registration successful"
    assert "seller_id" in data

    assert response.status_code == 201
    assert b"Seller registration successful" in response.data


def test_if_seller_login_successfully(test_client):
    payload = {
        "name": "amidat bread",
        "email": "amidat@gmail.com",
        "password": "password",
        "phone": "08123456781",
        "role": "seller"
    }


    with patch("app.routes.seller_controller.mail.send") as mock_send:
        register_response = test_client.post(
            "/api/sellers/register",
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert register_response.status_code == 201
        assert b"Seller registration successful" in register_response.data

    login_response = test_client.post(
        "/api/sellers/login",
        data=json.dumps({
            "email": "amidat@gmail.com",
            "password": "password"
        }),
        content_type='application/json'
    )

    assert login_response.status_code == 200
    assert b"Login successful" in login_response.data

def test_for_duplicate_email(test_client):
    payload = {
        "name": "Amidat",
        "email": "amidat@gmail.com",
        "password": "password123",
        "phone": "08123456789",
        "role": "seller"
    }

    with patch("app.routes.seller_controller.mail.send"):
        test_client.post(
            "/api/sellers/register",
            data=json.dumps(payload),
            content_type='application/json'
        )
        response = test_client.post(
            "/api/sellers/register",
            data=json.dumps(payload),
            content_type='application/json'
        )

    assert response.status_code == 409
    assert b"Seller email already registered" in response.data


def test_seller_register_with_invalid_email(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@wrong.com",
        "password": "password",
        "phone": "08125016091",
        "role" : "seller"
    }
    response = test_client.post("/api/sellers/register", data=json.dumps(payload), content_type="application/json")
    print("RESPONSE DATA:", response.status_code, response.data.decode())
    assert response.status_code == 400
    assert "email" in response.get_json().get("error", "").lower()

def test__register_with_invalid_phone(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone": "123456",
        "role":"seller"
    }
    response = test_client.post("/api/sellers/register", data=json.dumps(payload), content_type="application/json")
    print("RESPONSE DATA:", response.status_code, response.data.decode())
    assert response.status_code == 400
    assert "phone" in response.get_json().get("error", "").lower() or "Invalid phone" in response.get_data(as_text=True)
