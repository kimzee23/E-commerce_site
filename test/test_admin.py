import json

from bson import ObjectId
from flask import current_app

from app import mongo


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
    with test_client.application.app_context():
      mongo.db.users.delete_many({"email": "gazar@gmail.com", "role": "admin"})

    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone": "08125016091",
        "role": "admin"
    }
    response = test_client.post("/api/admins/register", data=json.dumps(payload), content_type='application/json')
    print("Response", response.status_code, response.data)
    assert response.status_code == 201

    login_payload = {
        "email": "gazar@gmail.com",
        "password": "password",
    }
    response = test_client.post("/api/admins/login", data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 201



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

def register_seller(client):
    seller_payload = {
        "name": "Test Seller",
        "email": "testseller@gmail.com",
        "password": "password",
        "phone": "08111111111",
        "role": "seller"
    }

    with client.application.app_context():
        from unittest.mock import patch
        with patch("app.routes.seller_controller.mail.send"):
            res = client.post("/api/sellers/register", data=json.dumps(seller_payload), content_type='application/json')
            assert res.status_code == 201
            return res.get_json()["seller_id"]


def test_suspend_seller_not_found(test_client):
    fake_id_ni = "64fc2ed4d1b1f3a9c1234567"
    response = test_client.put(f"/api/admins/suspend-seller/{fake_id_ni}")

    assert response.status_code == 404
    assert b"Seller not found" in response.data

def test_suspend_seller_success(test_client):
    seller_id = register_seller(test_client)

    response = test_client.put(f"/api/admins/suspend-seller/{seller_id}")
    assert response.status_code == 200
    assert b"Seller suspended successfully" in response.data

def test_delete_seller_success(test_client):
    seller_id = register_seller(test_client)

    response = test_client.delete(f"/api/admins/delete-seller/{seller_id}")
    assert response.status_code == 200
    assert b"Seller deleted successfully" in response.data

def test_delete_seller_not_found(test_client):
    fake_id = str(ObjectId())
    response = test_client.delete(f"/api/admins/delete-seller/{fake_id}")
    assert response.status_code == 404
    assert b"Seller not found" in response.data
