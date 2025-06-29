import json

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.dtos.request.user_request import UserRegisterRequest
from app.enums.user_role import UserRole
from app.services.userService import UserService
from app.utils.validator import validation_for_email, validation_for_phoneNumber

seller_bp = Blueprint('sellers', __name__, url_prefix='/api/sellers')

@seller_bp.route('/register', methods=['POST'])
def register_seller():
    data = request.get_json()
    try:
        user_data = UserRegisterRequest(**data)

        if not validation_for_email(user_data.email):
            return jsonify({"error": "Invalid email format"}), 400

        if not validation_for_phoneNumber(user_data.phone):
            return jsonify({"error": "Invalid phone number format"}), 400

        seller_id = UserService.register(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            phone=user_data.phone,
            role=UserRole.SELLER.value
        )
        return jsonify({"message": "Seller registration successful", "seller_id": seller_id}), 201

    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except ValueError as error:
        return jsonify({"error": str(error)}), 409
    except Exception as error:
        return jsonify({"error": "Unexpected error", "details": str(error)}), 500


@seller_bp.route('/login', methods=['POST'])
def login_seller():
    deta= request.get_json()
    try:
        seller_id,user = UserService.login(
            email=deta['email'],
            password=deta['password'],
            role= "seller"

            )
        return jsonify({"message":"Login successful","seller_id":seller_id}),200
    except ValueError as error:
        return jsonify({"error":str(error)}),401
    except Exception as error:
        return jsonify({"error": "Unexpected error", "details": str(error)}), 500
