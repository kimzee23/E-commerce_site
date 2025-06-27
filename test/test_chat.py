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
    assert response.status_code == 201


def test_get_conversation_success(test_client):
    product_id = str(ObjectId())
    buyer_id = str(ObjectId())
    response = test_client.get(f"/api/chat/conversation/{product_id}/{buyer_id}")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        messages = json.loads(response.data)
        assert isinstance(messages, dict)
    elif response.status_code == 404:
        data = json.loads(response.data)
        assert "error" in data