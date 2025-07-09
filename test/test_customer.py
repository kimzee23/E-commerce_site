import json
from unittest.mock import patch


def test_register_customer_successful(test_client):
    payload = {
        "name": "Ade",
        "email": "ade@gmail.com",
        "password": "password",
        "phone": "08150160911",
        "role": "customer"
    }

    with patch("app.routes.customer_controller.mail.send") as mock_send:
        response = test_client.post(
            "/api/customers/register",
            data=json.dumps(payload),
            content_type="application/json"
        )

        assert response.status_code == 201
        data = response.get_json()
        assert "customer_id" in data
        assert data["message"] == "Customer registered"



        mock_send.assert_called_once()
def test_register_duplicate_email(test_client):
    payload= {
        "name": "Ade",
        "email": "ade@gmail.com",
        "password": "maleek",
        "phone": "08150160911",
        "role": "customer"
    }
    test_client.post(
        "/api/customers/register", data=json.dumps(payload), content_type='application/json')
    response = test_client.post(
        "/api/customers/register", data=json.dumps(payload), content_type='application/json')

    assert response.status_code == 409
    assert b"Customer email already registered" in response.data

def test_customer_login_success(test_client):
    payload= {
        "name": "Ade",
        "email": "adewale@gmail.com",
        "password": "maleek",
        "phone": "08150160911",
        "role":"customer"
    }
    reg_response= test_client.post("/api/customers/register", data=json.dumps(payload), content_type='application/json')
    print("Register status:", reg_response.status_code)
    print("Register data:", reg_response.data.decode())
    login_payload= {
        "email": "adewale@gmail.com",
        "password": "maleek"
    }
    response = test_client.post("/api/customers/login", data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert "customer_id" in data

def test_admin_register_with_invalid_email(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@wrong.com",
        "password": "password",
        "phone": "081125016091",
        "role": "customer"
    }
    response = test_client.post("/api/customers/register", data=json.dumps(payload), content_type="application/json")
    print("Response:", response.status_code,response.data)
    assert response.status_code == 400
    assert "email" in response.get_json().get("error", "").lower()

def test_admin_register_with_invalid_phone(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone": "123456",
        "role":"customer"
    }
    response = test_client.post("/api/customers/register", data=json.dumps(payload), content_type="application/json")
    print("Response:", response.status_code,response.data)
    assert response.status_code == 400
    assert "phone" in response.get_json().get("error", "").lower() or "Invalid phone" in response.get_data(as_text=True)
