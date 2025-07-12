import json
from bson import ObjectId

def test_send_chat_message_success(test_client):
    payload = {
        "product_id": str(ObjectId()),
        "buyer_id": str(ObjectId()),
        "seller_id": str(ObjectId()),
        "message": "Can you sell it for ₦5000?",
        "price_offer": 5000
    }
    response = test_client.post("/api/chat/send", data=json.dumps(payload), content_type='application/json')
    print("Response JSON", response.get_json())
    assert response.status_code == 201



def test_get_conversation_success(test_client):
    product_id = str(ObjectId())
    buyer_id = str(ObjectId())
    seller_id = str(ObjectId())


    payload = {
        "product_id": product_id,
        "buyer_id": buyer_id,
        "seller_id": seller_id,
        "message": "Is it still available?",
        "price_offer": 9000
    }

    send_response = test_client.post("/api/chat/send", data=json.dumps(payload), content_type='application/json')
    assert send_response.status_code == 201


    get_response = test_client.get(f"/api/chat/conversation/{product_id}/{buyer_id}")
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert "messages" in data
    assert isinstance(data["messages"], list)
