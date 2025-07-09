
from pydantic import ValidationError

from flask import Blueprint, request, jsonify
from flask_mail import Message
from app import mail
from app.dtos.request.user_request import UserRegisterRequest
from app.enums.user_role import UserRole
from app.services.userService import UserService
from app.utils.validator import validation_for_email, validation_for_phoneNumber

customer_bp = Blueprint("customer_bp", __name__, url_prefix="/api/customers")

@customer_bp.route("/register", methods=["POST"])
def register_customer():
    data = request.get_json()
    try:
        validated_data = UserRegisterRequest(**data)

        if not validation_for_email(validated_data.email):
            return jsonify({"error": "Invalid email format"}), 400

        if not validation_for_phoneNumber(validated_data.phone):
            return jsonify({"error": "Invalid phone number format"}), 400

        customer_id, otp = UserService.register(
            name=validated_data.name,
            email=validated_data.email,
            password=validated_data.password,
            role=UserRole.CUSTOMER.value,
            phone=validated_data.phone
        )

        msg = Message(
            subject="Verify Your Account - OTP Inside!",
            recipients=[validated_data.email],
            body=(
                f"Hello {validated_data.name},\n\n"
                "Welcome to our E-commerce platform!\n\n"
                f"Here is your OTP code for verification: {otp}\n\n"
                "Enter this OTP to activate your account.\n\n"
                "Best regards,\nThe Team"
            )
        )
        mail.send(msg)

        return jsonify({
            "message": "Customer registered",
            "customer_id": customer_id
        }), 201

    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 422
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409
    except Exception as e:
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

