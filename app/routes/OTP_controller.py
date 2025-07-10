from flask import request, jsonify, Blueprint
from app.extentions import mongo

otp_bp = Blueprint("otp", __name__, url_prefix="/api/otp")

@otp_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.get("verified"):
        return jsonify({"message": "Already verified"}), 200

    if user.get("otp") == otp:
        mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"verified": True}})
        return jsonify({"message": "Email verified successfully"}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400
