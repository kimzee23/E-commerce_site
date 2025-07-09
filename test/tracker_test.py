import pytest
import json
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

def test_track_product_view(test_client, test_product_payload):
    create_response = test_client.post(
        '/api/products/create',
        json=test_product_payload
    )
    assert create_response.status_code == 201
    product_id = create_response.get_json()["product_id"]

    response = test_client.post(f'/api/product-tracker/view/{product_id}')
    print("View Response:", response.status_code, response.get_json())
    assert response.status_code == 200
    assert response.get_json()["message"] == "Product view tracked"

def test_track_product_purchase(test_client, test_product_payload):
    create_response = test_client.post(
        '/api/products/create',
        json=test_product_payload
    )
    assert create_response.status_code == 201
    product_id = create_response.get_json()["product_id"]

    response = test_client.post(f"/api/product-tracker/purchase/{product_id}")
    print("Purchase Response:", response.status_code, response.get_json())
    assert response.status_code == 201
    assert response.get_json()["message"] == "Product purchase tracked"

def test_get_product_tracker(test_client, test_product_payload):
    create_response = test_client.post(
        '/api/products/create',
        json=test_product_payload
    )
    assert create_response.status_code == 201
    product_id = create_response.get_json()["product_id"]

    test_client.post(f"/api/product-tracker/view/{product_id}")
    test_client.post(f"/api/product-tracker/purchase/{product_id}")

    tracker_response = test_client.get(f"/api/product-tracker/{product_id}")
    print("Tracker Response:", tracker_response.status_code, tracker_response.get_json())
    assert tracker_response.status_code == 200

    data = tracker_response.get_json()
    assert data["product_id"] == product_id
    assert data["views"] >= 1
    assert data["purchases"] >= 1
