from datetime import datetime, timezone
from bson import ObjectId
from app.extentions import mongo


class ProductTrackerService:
    @staticmethod
    def track_view(product_id):
        try:
            result = mongo.db.product_tracker.update_one(
                {"product_id": ObjectId(product_id)},
                {
                    "$inc": {"views": 1},
                    "$set": {"last_viewed": datetime.now(timezone.utc)}
                },
                upsert=True
            )
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            print("Error in tracker_view:", e)
            raise

    @staticmethod
    def tracker_purchase(product_id):
        print("Purchase tracker updated for product:", product_id)
        result = mongo.db.product_tracker.update_one(
            {"product_id": ObjectId(product_id)},
            {
                "$inc": {"purchases": 1},
                "$set": {"last_purchase": datetime.now(timezone.utc)}
            },
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None

    @staticmethod
    def get_tracker(product_id):
        print("Fetching tracker for product:", product_id)
        doc = mongo.db.product_tracker.find_one({"product_id": ObjectId(product_id)})
        return doc
