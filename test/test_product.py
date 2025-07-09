import json
import pytest
from bson import ObjectId
from flask_oauthlib.utils import create_response


@pytest.fixture
def test_product_payload():
    return {
        "name": "iPhone 18 Pro",
        "description": "Latest model with ultra camera",
        "price": 1200.00,
        "category": "electronics",
        "stock_quantity": 5,
        "seller_id": str(ObjectId()),
        "images": ["https://image.com/iphone18pro.jpg"]
    }

def test_that_seller_add_product_successfully(test_client, test_product_payload):
    response = test_client.post(
        '/api/products/create',
        data=json.dumps(test_product_payload),
        content_type='application/json'
    )

    print("Response JSON:", response.get_json(), flush=True)
    assert response.status_code == 201
    data = response.get_json()
    assert "product_id" in data
    assert data["message"] == "Product created successfully"


def test_create_product_missing_fields_should_fail(test_client):
    payload = {
        "name": "iPhone 18 Pro",
        "description": "Missing images field test",
        "price": 1000,
        "category": "electronics",
        "stock_quantity": 10,
        "seller_id": str(ObjectId()),
        # "images" field is ment  to a trigger validation error
    }

    response = test_client.post(
        "/api/products/create",
        data=json.dumps(payload),
        content_type='application/json'
    )

    print("RESPONSE:", response.status_code, response.data.decode())
    assert response.status_code == 422
    data = response.get_json()
    missing_fields = {error["loc"][0] for error in data["details"] if error["type"] == "missing"}

    assert "images" in missing_fields
def test_get_all_products_is_working(test_client, test_product_payload):
    Create_response = test_client.post(
        '/api/products/create',
        data=json.dumps(test_product_payload),
        content_type='application/json'
    )
    assert Create_response.status_code == 201

    get_response = test_client.get('/api/products/')
    print("GET ALL PRODUCTS RESPONSE:", get_response.status_code, get_response.get_json())

    assert get_response.status_code == 200
    data = get_response.get_json()
    assert isinstance(data, list)
    assert any(prod["name"] == test_product_payload["name"] for prod in data)

def test_get_product_by_id_method_is_working(test_client, test_product_payload):
    Create_response = test_client.post(
        '/api/products/create',
        data=json.dumps(test_product_payload),
        content_type='application/json'
    )
    print("Response:", Create_response.status_code, Create_response.data.decode())
    assert Create_response.status_code == 201

    product_id = Create_response.get_json()["product_id"]

    get_response = test_client.get(f'/api/products/{product_id}')
    print("GET PRODUCT BY ID RESPONSE:", get_response.status_code, get_response.get_json())

    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data["id"] == product_id
    assert data["name"] == test_product_payload["name"]

def test_that_update_product_method_is_working(test_client, test_product_payload):
    Create_response = test_client.post(
        '/api/products/create',
        data=json.dumps(test_product_payload),
        content_type='application/json'
    )
    print("Create Response:", Create_response.status_code, Create_response.data.decode())
    assert Create_response.status_code == 201
    product_id = Create_response.get_json()["product_id"]
    seller_id = test_product_payload["seller_id"]
    update_payload = {
        "seller_id": seller_id,
        "update_fields": {
            "name": "iPhone 18 Pro Max",
            "price": 1200.00,
            "stock_quantity": 5
        }
    }
    update_response = test_client.put(
        f'/api/products/{product_id}/update',
        data=json.dumps(update_payload),
        content_type='application/json'
    )
    print("UPDATE PRODUCT RESPONSE:", update_response.status_code, update_response.data.decode())
    assert update_response.status_code == 200

def test_get_product_by_name_method_is_working(test_client, test_product_payload):
    Create_response = test_client.post(
        '/api/products/create',
        data=json.dumps(test_product_payload),
        content_type='application/json'
    )
    print("Create Response:", Create_response.status_code, Create_response.data.decode())
    assert Create_response.status_code == 201

    product_name = test_product_payload["name"]

    get_response = test_client.get(f'/api/products/search?name={product_name}')
    print("GET PRODUCT BY NAME RESPONSE:", get_response.status_code, get_response.get_json())

    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data["name"] == product_name

def test_delete_product_is_working(test_client, test_product_payload):
    Create_response = test_client.post(
        '/api/products/create',
        data=json.dumps(test_product_payload),
        content_type='application/json'
    )
    assert Create_response.status_code == 201
    product_id = Create_response.get_json()["product_id"]
    seller_id = test_product_payload["seller_id"]
    delete_payload = {"seller_id": seller_id}
    delete_response = test_client.delete(
        f'/api/products/{product_id}',
        data=json.dumps(delete_payload),
        content_type='application/json'
    )
    print("DELETE RESPONSE:", delete_response.status_code, delete_response.data.decode())
    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Product deleted successfully"
    get_response = test_client.get(f'/api/products/{product_id}')
    print("GET AFTER DELETE:", get_response.status_code, get_response.data.decode())
    assert get_response.status_code == 404




