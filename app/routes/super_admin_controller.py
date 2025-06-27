
from flask import Blueprint, request, jsonify

from app.services.userService import UserService

from flask import Blueprint, request, jsonify
from app.services.userService import UserService
from app.utils.validator import validation_for_email, validation_for_phoneNumber

superAdmin_bp = Blueprint("superAdmin", __name__, url_prefix="/api/superAdmin")

@superAdmin_bp.route("/register", methods=["POST"])
def register_superAdmin():
    data = request.get_json()
    try:
        if not validation_for_email(data["email"]):
            print("Email failed validation")
            return jsonify({"error": "Invalid email format"}), 400

        if not validation_for_phoneNumber(data["phone"]):
            print("Phone failed validation")
            return jsonify({"message": "Invalid phone number format"}), 400

        superAdmin_id = UserService.register(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phone=data["phone"],
            role="superAdmin"
        )
        return jsonify({
            "message": "SuperAdmin Registration Successful",
            "superAdmin_id": superAdmin_id
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": "Unexpected", "details": str(e)}), 500




@superAdmin_bp.route("/login", methods=["POST"])
def login_superAdmin():
    data = request.get_json()
    try:
        superAdmin_id, user = UserService.login(
            email=data["email"],
            password=data["password"],
            role="superAdmin"
        )
        return jsonify({
            "message": "SuperAdmin Login Successful",
            "superAdmin_id": superAdmin_id
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Unexpected", "details": str(e)}), 500
