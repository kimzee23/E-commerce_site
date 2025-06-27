from flask import Blueprint, request, jsonify
from app.services.userService import UserService
from app.utils.validator import validation_for_email, validation_for_phoneNumber


buyer_bp = Blueprint("buyer", __name__, url_prefix="/api/buyers")

@buyer_bp.route("/register", methods=["POST"])
def register_buyer():
    data = request.get_json()
    try:
        if not validation_for_email(data["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        if not validation_for_phoneNumber(data["phone"]):
            return jsonify({"error": "Invalid phone number format"}), 400

        buyer_id = UserService.register(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phone=data["phone"],
            role="buyer"
        )
        return jsonify({"message": "Buyer registered successfully", "buyer_id": buyer_id}), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 409
    except Exception as error:
        return jsonify({"error": "Unexpected error", "details": str(error)}), 500

@buyer_bp.route("/login", methods=["POST"])
def login_buyer():
    data = request.get_json()
    try:
        if not validation_for_email(data["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        buyer_id, _ = UserService.login(
            email=data["email"],
            password=data["password"],
            role="buyer"
        )
        return jsonify({"message": "Buyer login successful", "buyer_id": buyer_id}), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 401
    except Exception as error:
        return jsonify({"error": "Unexpected error", "details": str(error)}), 500
