from datetime import datetime
from bson import ObjectId

class ProductTracker:
    def __init__(self, product_id, views=0, purchases=0, last_viewed=None, last_purchased=None):
        self.product_id = ObjectId(product_id)
        self.views = views
        self.purchases = purchases
        self.last_viewed = last_viewed or datetime.utcnow()
        self.last_purchased = last_purchased or datetime.utcnow()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "views": self.views,
            "purchases": self.purchases,
            "last_viewed": self.last_viewed,
            "last_purchased": self.last_purchased
        }
