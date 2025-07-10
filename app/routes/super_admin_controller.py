from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, request, jsonify
from app.services.userService import UserService
from app import mongo

superAdmin_bp = Blueprint("superAdmin", __name__, url_prefix="/api/superAdmin")


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


@superAdmin_bp.route('/suspend-user/<user_id>', methods=['PUT'])
def suspend_user(user_id):
    try:
        try:
            obj_id = ObjectId(user_id)
        except InvalidId:
            return jsonify({"error": "Invalid ObjectId"}), 400

        user = mongo.db.users.find_one({"_id": obj_id})
        print("User found before suspend:", user)

        result = mongo.db.users.update_one(
            {"_id": obj_id},
            {"$set": {"is_active": False}}
        )
        if result.modified_count:
            return jsonify({"message": "User suspended successfully"}), 200
        return jsonify({"error": "User not found or already suspended"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@superAdmin_bp.route('/unsuspend-user/<user_id>', methods=['PUT'])
def unsuspend_user(user_id):
    try:
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": True}}
        )
        if result.modified_count:
            return jsonify({"message": "User unsuspended successfully"}), 200
        return jsonify({"error": "User not found or already active"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@superAdmin_bp.route('/delete-user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            return jsonify({"message": "User deleted successfully"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
