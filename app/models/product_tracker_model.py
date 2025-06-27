from datetime import datetime
from bson import ObjectId

class ProductTracker:
    def __init__(self, product_id, user_id=None, event_type="view"):
        self.product_id = ObjectId(product_id)
        self.user_id = ObjectId(user_id) if user_id else None
        self.event_type = event_type  # view or purchase
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
        }
