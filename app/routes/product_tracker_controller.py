from flask import Blueprint, jsonify
from app.services.Tracker_service import ProductTrackerService

product_tracker_bp = Blueprint("product_tracker_bp", __name__, url_prefix="/api/product-tracker")
@product_tracker_bp.post("/view/<product_id>")
def track_product_view(product_id):
    try:
        ProductTrackerService.track_view(product_id)
        return jsonify({"message": "Product view tracked"}), 200
    except Exception as error:
        return jsonify({"error": "Failed to track view", "details": str(error)}), 500


@product_tracker_bp.route('/purchase/<product_id>', methods=['POST'])
def track_purchase(product_id):
    try:
        ProductTrackerService.tracker_purchase(product_id)
        return jsonify({"message": "Product purchase tracked"}), 201
    except Exception as e:
        return jsonify({"error": "Failed to track purchase", "details": str(e)}), 500


@product_tracker_bp.get("/<product_id>")
def get_track_product(product_id):
    try:
        tracker = ProductTrackerService.get_tracker(product_id)
        if not tracker:
            return jsonify({"message": "Product not found"}), 404

        tracker_data = {
            "product_id": str(tracker["product_id"]),
            "views": tracker.get("views", 0),
            "purchases": tracker.get("purchases", 0),
            "last_viewed": tracker.get("last_viewed"),
            "last_purchase": tracker.get("last_purchase")
        }

        return jsonify(tracker_data), 200
    except Exception as error:
        return jsonify({"error": "Failed to track product", "details": str(error)}), 500

