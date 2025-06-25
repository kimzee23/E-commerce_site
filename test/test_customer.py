import json
import time


def test_register_customer_success(test_client):
    payload= {
        "name": "Ade",
        "email": "ade@gmail.com",
        "password": "password"
    }
    responseOne = test_client.post("/api/customers/register", data=json.dumps(payload), content_type='application/json')
    assert responseOne.status_code == 201
    data = json.loads(responseOne.data)
    assert "customer_id" in data

def test_register_duplicate_email(test_client):
    payload= {
        "name": "Ade",
        "email": "ade@gmail.com",
        "password": "password"
    }
    test_client.post(
        "/api/customers/register", data=json.dumps(payload), content_type='application/json')
    response = test_client.post(
        "/api/customers/register", data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 409
    assert b"Email already registered" in response.data

def test_customer_login_success(test_client):
    payload= {
        "name": "Ade",
        "email": "ade@gmail.com",
        "password": "password"
    }
    test_client.post("/api/customers/register", data=json.dumps(payload), content_type='application/json')
    time.sleep(0.1)
    payload= {
        "email": "ade@gmail.com",
        "password": "password"
    }
    responseThree = test_client.post("/api/customers/login", data=json.dumps(payload), content_type='application/json')
    assert responseThree.status_code == 200
    data = json.loads(responseThree.data)
    assert "message" in data
    assert "customer_id" in data