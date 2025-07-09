import json
from unittest.mock import patch

from bson import ObjectId

from app.models.user_model import User
from werkzeug.security import generate_password_hash
from app import mongo  # make sure this is available

def test_superadmin_login_success(test_client):

    superadmin_user = User(
        name="Boss",
        email="boss@gmail.com",
        password=generate_password_hash("password"),
        phone="08099999000",
        role="super_admin"
    )
    mongo.db.users.insert_one(superadmin_user.to_dict())

    login_payload = {
        "email": "boss@gmail.com",
        "password": "password"
    }

    response = test_client.post(
        "/api/superAdmin/login",
        data=json.dumps(login_payload),
        content_type='application/json'
    )

    print("LOGIN RESPONSE:", response.status_code, response.data.decode())
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "superAdmin_id" in data

def register_sample_user(test_client, role, email, phone):
    payload = {
        "name": f"{role} User",
        "email": email,
        "password": "password",
        "phone": phone,
        "role": role
    }

    url = f"/api/{role}s/register"
    response = test_client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json"
    )

    print("REGISTER RESPONSE:", response.status_code, response.data.decode())
    data = json.loads(response.data)

    raw_id = data.get(f"{role}_id") or data.get("seller_id")
    if isinstance(raw_id, list):
        return raw_id[0]  # Mongo ID
    return raw_id


def test_suspend_seller_success(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        seller_id = register_sample_user(test_client, "seller", "seller1@gmail.com", "08000000001")
        response = test_client.put(f"/api/superAdmin/suspend-user/{seller_id}")
        assert response.status_code == 200
        assert "suspended" in response.get_json()["message"].lower()


def test_unsuspend_seller_success(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        seller_id = register_sample_user(test_client, "seller", "seller2@gmail.com", "08000000002")
        test_client.put(f"/api/superAdmin/suspend-user/{seller_id}")
        response = test_client.put(f"/api/superAdmin/unsuspend-user/{seller_id}")
        assert response.status_code == 200
        assert "unsuspended" in response.get_json()["message"].lower()

def test_delete_seller_success(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        seller_id = register_sample_user(test_client, "seller", "seller3@yahoo.com", "08000000003")
        response = test_client.delete(f"/api/superAdmin/delete-user/{seller_id}")
        assert response.status_code == 200
        assert "deleted" in response.get_json()["message"].lower()



# Admin testing

def test_suspend_Admin_success(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        admin_id = register_sample_user(test_client, "admin", "Admin1@gmail.com", "08000000004")
        response = test_client.put(f"/api/superAdmin/suspend-user/{admin_id}")
        assert response.status_code == 200
        assert "suspended" in response.get_json()["message"].lower()

def test_unsuspend_Admin_success(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        Admin_id = register_sample_user(test_client, "admin", "Admin2@gmail.com", "08000000005")
        test_client.put(f"/api/superAdmin/suspend-user/{Admin_id}")
        response = test_client.put(f"/api/superAdmin/unsuspend-user/{Admin_id}")
        assert response.status_code == 200
        assert "unsuspended" in response.get_json()["message"].lower()

def test_delete_Admin_success(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        admin_id = register_sample_user(test_client, "admin", "Admin3@yahoo.com", "08000000006")
        response = test_client.delete(f"/api/superAdmin/delete-user/{admin_id}")
        assert response.status_code == 200
        assert "deleted" in response.get_json()["message"].lower()

# not found


def test_suspend_user_not_found(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        fake_id = str(ObjectId())
        response = test_client.put(f"/api/superAdmin/suspend-user/{fake_id}")
        assert response.status_code == 404
        assert "not found" in response.get_json()["error"].lower()

def test_unsuspend_user_not_found(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        fake_id = str(ObjectId())
        response = test_client.put(f"/api/superAdmin/unsuspend-user/{fake_id}")
        assert response.status_code == 404
        assert "not found" in response.get_json()["error"].lower()

def test_delete_user_not_found(test_client):
    with patch("app.routes.seller_controller.mail.send"):
        fake_id = str(ObjectId())
        response = test_client.delete(f"/api/superAdmin/delete-user/{fake_id}")
        assert response.status_code == 404
        assert "not found" in response.get_json()["error"].lower()
