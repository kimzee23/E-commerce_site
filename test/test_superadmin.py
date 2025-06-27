import json

def test_superadmin_register_is_successful(test_client):
    payload = {
        "name": "Boss",
        "email": "boss@gmail.com",
        "password": "password",
        "phone": "08099999000"
    }
    response = test_client.post(
        "/api/superAdmin/register",
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "superAdmin_id" in data

def test_superAdmin_login_success(test_client):
    payload = {
        "name": "Boss",
        "email": "boss@gmail.com",
        "password": "password",
        "phone": "08010099999"
    }
    test_client.post("/api/superAdmin/register", data=json.dumps(payload), content_type='application/json')

    login_payload = {
        "email": "boss@gmail.com",
        "password": "password",
    }
    response = test_client.post("/api/superAdmin/login", data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "superAdmin_id" in data
def test_admin_register_with_invalid_email(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@@wrong.com",
        "password": "password",
        "phone": "081125016091"
    }
    response = test_client.post("/api/superAdmin/register", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "email" in response.get_json().get("error", "").lower()

def test_admin_register_with_invalid_phone(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone": "123456"
    }
    response = test_client.post("/api/superAdmin/register", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "phone" in response.get_json().get("error", "").lower() or "Invalid phone" in response.get_data(as_text=True)
