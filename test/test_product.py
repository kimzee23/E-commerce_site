import json
import pytest
from bson import ObjectId

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

    # Assert the HTTP status code for validation error
    assert response.status_code == 422

    # Parse response JSON and verify missing field is reported
    data = response.get_json()
    missing_fields = {error["loc"][0] for error in data["details"] if error["type"] == "missing"}

    assert "images" in missing_fields
