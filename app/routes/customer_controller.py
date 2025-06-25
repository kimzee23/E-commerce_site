from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash

from app.services.customer_service import CustomerService

customer_bp = Blueprint("customer_bp", __name__, url_prefix="/api/customers")

@customer_bp.route("/register", methods=["POST"])
def register_customer():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        customer_id = CustomerService.register_customer(name, email, password)
        return jsonify({"message": "Customer registered", "customer_id": customer_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

@customer_bp.route("/login", methods=["POST"])
def login_customer():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email or password"}), 400
    mongo = current_app.mongo
    user = mongo.db.users.find_one({"email": email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401
    return jsonify({"customer_id": user["customer_id"]}), 200