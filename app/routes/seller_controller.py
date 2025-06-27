import json

from flask import Blueprint, request, jsonify

from app.services.userService import UserService
from app.utils.validator import validation_for_email, validation_for_phoneNumber

seller_bp = Blueprint('seller', __name__, url_prefix='/api/sellers')

@seller_bp.route('/register', methods=['POST'])
def register_seller():
    data = request.get_json()
    try:
        if not validation_for_email(data["email"]):
            print("Email failed validation")
            return jsonify({"error": "Invalid email format"}), 400

        if not validation_for_phoneNumber(data["phone"]):
            print("Phone failed validation")
            return jsonify({"message": "Invalid phone number format"}), 400

        seller_id = UserService.register(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            phone=data['phone'],
            role="seller"
        )
        return jsonify({"massage":"seller registration successful","seller_id":seller_id}),201
    except ValueError as error:
        return jsonify({"error":str(error)}),409
    except Exception as error:
        return jsonify({"massage":"Unexpected","details":str(error)}),500

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
