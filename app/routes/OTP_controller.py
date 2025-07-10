from flask import request, jsonify, Blueprint
from app.dtos.request.otp_request import VerifyOtpRequest
from app.services.otp_service import OtpService

otp_bp = Blueprint("otp", __name__, url_prefix="/api/otp")

@otp_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    try:
        data = VerifyOtpRequest(**request.get_json())
        message = OtpService.verify(str(data.email).strip(), str(data.otp).strip())
        return jsonify({"message": message}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404 if str(ve) == "User not found" else 400
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

