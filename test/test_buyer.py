import json

def test_buyer_register_success(test_client):
    payload = {
        "name": "John",
        "email": "john@gmail.com",
        "password": "password",
        "phone": "08112223344",
        "role": "buyer"
    }
    response = test_client.post(
        "/api/buyers/register",
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "buyer_id" in data or "id" in data

def test_buyer_register_duplicate_email(test_client):
    payload = {
        "name": "John",
        "email": "john@gmail.com",
        "password": "password",
        "phone": "08112223344",
        "role": "buyer"
    }
    test_client.post("/api/buyers/register", data=json.dumps(payload), content_type='application/json')
    response = test_client.post("/api/buyers/register", data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 409

def test_buyer_login_success(test_client):
    payload = {
        "name": "suliha",
        "email": "suliha@gmail.com",
        "password": "mypassword",
        "phone": "08115556677",
        "role": "buyer"
    }
    response=test_client.post("/api/buyers/register", data=json.dumps(payload), content_type='application/json')
    print("Response:", response.status_code,response.data)
    login_payload = {
        "email": "suliha@gmail.com",
        "password": "mypassword"
    }
    response = test_client.post("/api/buyers/login", data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 200 or response.status_code == 201
    data = json.loads(response.data)
    assert "buyer_id" in data or "id" in data

def test_buyer_login_invalid_password(test_client):
    login_payload = {
        "email": "john@gmail.com",
        "password": "password123"
    }
    response = test_client.post("/api/buyers/login", data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 401
