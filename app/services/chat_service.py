from bson import ObjectId
from app import mongo
from app.models.chat_model import Chat
from datetime import datetime, timezone


class ChatService:

    @staticmethod
    def start_chat(buyer_id, seller_id, product_id):
        chat = Chat(buyer_id=buyer_id, seller_id=seller_id, product_id=product_id)
        result = mongo.db.chats.insert_one(chat.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def send_message(product_id, buyer_id, seller_id, message, price_offer):
        db = mongo.db

        chat = db.chats.find_one({
            "product_id": ObjectId(product_id),
            "buyer_id": ObjectId(buyer_id),
            "seller_id": ObjectId(seller_id)
        })

        if not chat:
            chat_id = ChatService.start_chat(buyer_id, seller_id, product_id)
        else:
            chat_id = chat["_id"]

        new_message = {
            "sender_id": ObjectId(buyer_id),
            "message": message,
            "price_offer": price_offer,
            "timestamp": datetime.now(timezone.utc)
        }

        result = db.chats.update_one(
            {"_id": ObjectId(chat_id)},
            {"$push": {"messages": new_message}}
        )

        if result.modified_count == 1:
            return new_message
        else:
            raise ValueError("Message not saved.")

    @staticmethod
    def get_chat(chat_id):
        db = mongo.db
        chat = db.chats.find_one({"_id": ObjectId(chat_id)})
        if not chat:
            raise ValueError("Chat not found")
        return chat

    @staticmethod
    def get_chats_for_user(user_id):
        db = mongo.db
        chats = db.chats.find({
            "$or": [
                {"buyer_id": ObjectId(user_id)},
                {"seller_id": ObjectId(user_id)}
            ]
        })
        return list(chats)

    @staticmethod
    def get_conversation(product_id, buyer_id):
        db = mongo.db
        chat = db.chats.find_one({
            "product_id": ObjectId(product_id),
            "buyer_id": ObjectId(buyer_id)
        })

        if not chat:
            raise ValueError("Chat not found")

        conversation = {
            "chat_id": str(chat["_id"]),
            "buyer_id": str(chat["buyer_id"]),
            "seller_id": str(chat["seller_id"]),
            "product_id": str(chat["product_id"]),
            "created_at": chat["created_at"].isoformat(),
            "messages": [
                {
                    "sender_id": str(m["sender_id"]),
                    "message": m["message"],
                    "price_offer": m.get("price_offer"),
                    "timestamp": m["timestamp"].isoformat()
                }
                for m in chat.get("messages", [])
            ]
        }

        return conversation
