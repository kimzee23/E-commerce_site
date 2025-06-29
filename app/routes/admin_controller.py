from flask import Blueprint, request, jsonify

from app.enums.user_role import UserRole
from app.services.userService import UserService
from email_validator import EmailNotValidError

from app.utils.validator import validation_for_email, validation_for_phoneNumber

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admins')


@admin_bp.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    print("Incoming data:", data)
    try:
        if not validation_for_email(data["email"]):
            print("Email failed validation")
            return jsonify({"error": "Invalid email format"}), 400

        if not validation_for_phoneNumber(data["phone"]):
            print("Phone failed validation")
            return jsonify({"message": "Invalid phone number format"}), 400

        admin_id = UserService.register(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            phone=data['phone'],
            role=UserRole.ADMIN.value,
        )
        return jsonify({"message": "Admin Registration Successful", "admin_id": admin_id}), 201


    except ValueError as error:
        return jsonify({"message": str(error)}), 409
    except Exception as error:
        return jsonify({"message": "Unexpected error", "details": str(error)}), 500


@admin_bp.route('/login', methods=['POST'])
def login_admin():
    data = request.get_json()
    try:

        try:
            validation_for_email(data["email"])
        except EmailNotValidError as e:
            return jsonify({"message": "Invalid email format", "details": str(e)}), 400

        admin_id = UserService.login(
            email=data['email'],
            password=data['password'],
            role="admin"
        )
        return jsonify({"message": "Admin Login Successful", "admin_id": admin_id}), 201

    except ValueError as error:
        return jsonify({"message": str(error)}), 409
    except Exception as error:
        return jsonify({"message": "Unexpected error", "details": str(error)}), 500
