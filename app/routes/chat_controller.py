from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from bson import ObjectId

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")

@chat_bp.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    try:
        message_id = ChatService.send_message(
            product_id=data["product_id"],
            buyer_id=data["buyer_id"],
            seller_id=data["seller_id"],
            message=data["message"],
            price_offer=float(data["price_offer"])
        )
        return jsonify({"message": "Message sent", "message_id": message_id}), 201
    except Exception as e:
        return jsonify({"error": "Failed to send message", "details": str(e)}), 500

@chat_bp.route("/conversation/<product_id>/<buyer_id>", methods=["GET"])
def get_conversation(product_id, buyer_id):
    try:
        messages = ChatService.get_conversation(product_id, buyer_id)
        return jsonify(messages), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 404
    except Exception as error:
        return jsonify({"error": "Failed to fetch conversation", "details": str(error)}), 500
