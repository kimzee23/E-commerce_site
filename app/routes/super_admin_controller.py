
from flask import Blueprint, request, jsonify
from pydantic.v1 import ValidationError

from app.dtos.request.user_request import UserRegisterRequest
from app.enums.user_role import UserRole
from app.services.userService import UserService

from flask import Blueprint, request, jsonify
from app.services.userService import UserService
from app.utils.validator import validation_for_email, validation_for_phoneNumber

superAdmin_bp = Blueprint("superAdmin", __name__, url_prefix="/api/superAdmin")


@superAdmin_bp.route("/register", methods=["POST"])
def register_superAdmin():
    try:
        data = request.get_json()
        user_data = UserRegisterRequest(**data)
        if not validation_for_email(user_data.email):
            return jsonify({"error": "Invalid email format"}), 400

        if not validation_for_phoneNumber(user_data.phone):
            return jsonify({"error": "Invalid phone number format"}), 400

        superAdmin_id = UserService.register(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            phone=user_data.phone,
            role=UserRole.SUPER_ADMIN.value,
        )
        return jsonify({
            "message": "Superadmin Registration Successful",
            "superAdmin_id": superAdmin_id
        }), 201

    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 422
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500



@superAdmin_bp.route("/login", methods=["POST"])
def login_superAdmin():
    data = request.get_json()
    try:
        superAdmin_id, user = UserService.login(
            email=data["email"],
            password=data["password"],
            role="super_admin"
        )

        return jsonify({
            "message": "SuperAdmin Login Successful",
            "superAdmin_id": superAdmin_id
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Unexpected", "details": str(e)}), 500
