import json


def test_seller_register_is_successful(test_client):
    payload = {
        'name': "amidat bread",
        'email': "amidat@gmail.com",
        'password': "password",
        "phone": "0812345678"
    }
    response = test_client.post(
        '/api/sellers/register',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 201

def test_if_seller_login_successfully(test_client):
    payload = {
        "name": "amidat bread",
        "email": "amidat@gmail.com",
        "password": "password",
        "phone": "0812345678"
    }
    register_response = test_client.post(
        "/api/sellers/register", data=json.dumps(payload), content_type='application/json')
    assert register_response.status_code == 201

    login_payload = {
        "email": "amidat@gmail.com",
        "password": "password",
    }
    response = test_client.post("/api/sellers/login", data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert  "seller_id" in data

def test_for_duplicate_email(test_client):
    payload = {
        "name": "jerry",
        "email": "amidat@gmail.com",
        "password": "password",
        "phone": "0812345672"
    }
    test_client.post("/api/sellers/register", data=json.dumps(payload), content_type='application/json')
    response = test_client.post("/api/sellers/register", data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 409
    assert b"Email already registered" in response.data

def test_admin_register_with_invalid_email(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@@wrong.com",
        "password": "password",
        "phone": "081125016091"
    }
    response = test_client.post("/api/sellers/register", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "email" in response.get_json().get("error", "").lower()

def test_admin_register_with_invalid_phone(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone": "123456"
    }
    response = test_client.post("/api/sellers/register", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "phone" in response.get_json().get("error", "").lower() or "Invalid phone" in response.get_data(as_text=True)
