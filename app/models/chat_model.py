from datetime import datetime, timezone
from bson import ObjectId

class Chat:
    def __init__(self, buyer_id, seller_id, product_id, messages=None):
        self.buyer_id = ObjectId(buyer_id)
        self.seller_id = ObjectId(seller_id)
        self.product_id = ObjectId(product_id)
        self.messages = messages if messages else []
        self.created_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "product_id": self.product_id,
            "messages": self.messages,
            "created_at": self.created_at,
        }
