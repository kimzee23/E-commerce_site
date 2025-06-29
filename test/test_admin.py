import json


def test_if_admin_register_successfully(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone" : "08125016091",
        "role": "admin"
    }
    response = test_client.post("/api/admins/register", data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "admin_id" in data

def test_if_admin_login_successfully(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone" : "08125016091",
        "role": "admin"
    }
    response = test_client.post("/api/admins/register", data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201

    login_payload = {
        "email": "gazar@gmail.com",
        "password": "password",
    }
    response = test_client.post("/api/admins/login", data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "admin_id" in data

def test_admin_register_with_invalid_email(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@@mail.com",
        "password": "password",
        "phone": "081125016091",
        "role": "admin"

    }
    response = test_client.post("/api/admins/register", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "email" in response.get_json().get("error", "").lower()

def test_admin_register_with_invalid_phone(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone": "123456",
        "role": "admin"
    }
    response = test_client.post("/api/admins/register", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "phone" in response.get_json().get("error", "").lower() or "Invalid phone" in response.get_data(as_text=True)
