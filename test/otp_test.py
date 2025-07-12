from datetime import datetime, timezone

import pytest
import json
from bson import ObjectId
from app.extentions import mongo

def test_if_admin_register_successfully(test_client):
    payload = {
        "name": "gazar",
        "email": "gazar@gmail.com",
        "password": "password",
        "phone": "08125016091",
        "role": "admin"
    }
    response = test_client.post("/api/admins/register", data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "admin_id" in data


def test_verify_otp_success(test_client):
    test_email = "verifytest@gmail.com"
    otp_code = "123456"
    now = datetime.now(timezone.utc)

    user = {
        "_id": ObjectId(),
        "email": test_email,
        "otp": otp_code,
        "otp_created_at": now,
        "verified": False
    }
    mongo.db.users.insert_one(user)

    payload = {
        "email": test_email,
        "otp": otp_code
    }

    response = test_client.post(
        "/api/otp/verify-otp",
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Email verified successfully"

def test_verify_otp_invalid_otp(test_client):
    test_email = "verifytest@gmail.com"
    user = {
        "_id": ObjectId(),
        "email": test_email,
        "otp": "123456",
        "verified": False
    }
    mongo.db.users.insert_one(user)

    payload = {
        "email": test_email,
        "otp": "654321"  # wrong OTP
    }

    response = test_client.post("/api/otp/verify-otp", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert "Invalid OTP" in response.get_json()["error"]
    mongo.db.users.delete_one({"email": test_email})


def test_verify_otp_already_verified(test_client):
    test_email = "already@gmail.com"
    user = {
        "_id": ObjectId(),
        "email": test_email,
        "otp": "123456",
        "verified": True
    }
    mongo.db.users.insert_one(user)

    payload = {
        "email": test_email,
        "otp": "123456"
    }

    response = test_client.post("/api/otp/verify-otp", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Already verified"
    mongo.db.users.delete_one({"email": test_email})


def test_verify_otp_user_not_found(test_client):
    payload = {
        "email": "notfound@gmail.com",
        "otp": "123456"
    }

    response = test_client.post("/api/otp/verify-otp", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 404
    assert "User not found" in response.get_json()["error"]

def test_verify_otp_expired(test_client):
    from datetime import timedelta

    test_email = "expiredotp@gmail.com"
    otp_code = "999999"
    expired_time = datetime.now(timezone.utc) - timedelta(seconds=91)

    user = {
        "_id": ObjectId(),
        "email": test_email,
        "otp": otp_code,
        "otp_created_at": expired_time,
        "verified": False
    }
    mongo.db.users.insert_one(user)

    payload = {
        "email": test_email,
        "otp": otp_code
    }

    response = test_client.post(
        "/api/otp/verify-otp",
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert "Verification time passed" in response.get_json()["error"]
