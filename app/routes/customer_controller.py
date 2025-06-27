from flask import Blueprint, request, jsonify, current_app
from app.services.userService import UserService
from app.utils.validator import validation_for_email, validation_for_phoneNumber

customer_bp = Blueprint("customer_bp", __name__, url_prefix="/api/customers")

@customer_bp.route("/register", methods=["POST"])
def register_customer():
    data = request.get_json()
    try:
        if not validation_for_email(data["email"]):
            print("Email failed validation")
            return jsonify({"error": "Invalid email format"}), 400

        if not validation_for_phoneNumber(data["phone"]):
            print("Phone failed validation")
            return jsonify({"message": "Invalid phone number format"}), 400

        customer_id = UserService.register(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            role="customer",
            phone=data.get("phone")
        )
        return jsonify({"message": "Customer registered", "customer_id": customer_id}), 201
    except ValueError as e:
        print("Registration Error:", str(e))
        return jsonify({"error": str(e)}), 409

    except Exception as e:
        print("Unexpected Error:", str(e))
        return jsonify({"error": "Registration failed", "details": str(e)}), 500


@customer_bp.route("/login", methods=["POST"])
def login_customer():
    data = request.get_json()
    try:
        customer_id, user = UserService.login(
            email=data["email"],
            password=data["password"],
            role="customer"
        )
        return jsonify({"message": "Login successful", "customer_id": customer_id}), 200
    except ValueError as e:
        print("Login Error (ValueError):", str(e))
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        print("Login Error (Unexpected):", str(e))
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

