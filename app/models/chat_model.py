from datetime import datetime, timezone
from bson import ObjectId

class Chat:
    def __init__(self, buyer_id, seller_id, product_id, created_at=None, messages=None, _id=None):
        self.id = _id
        self.buyer_id = ObjectId(buyer_id)
        self.seller_id = ObjectId(seller_id)
        self.product_id = ObjectId(product_id)
        self.created_at = created_at or datetime.now(timezone.utc)
        self.messages = messages or []

    def to_dict(self):
        return {
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "product_id": self.product_id,
            "created_at": self.created_at,
            "messages": self.messages
        }

    @staticmethod
    def from_dict(data):
        return Chat(
            buyer_id=data.get("buyer_id"),
            seller_id=data.get("seller_id"),
            product_id=data.get("product_id"),
            created_at=data.get("created_at"),
            messages=data.get("messages", []),
            _id=data.get("_id")
        )
