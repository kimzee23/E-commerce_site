from flask import request, jsonify, Blueprint
from flask_mail import Message

from app.extentions import mongo, mail
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

@otp_bp.route("/resend", methods=["POST"])
def resend_otp():
    try:
        email = request.json.get("email")
        user = mongo.db.users.find_one({"email": email})
        if not user:
            raise ValueError("User not found")

        otp_code = OtpService.generate_otp(str(user["_id"]))

        msg = Message(
            subject="Your new OTP",
            recipients=[email],
            body=f"Hello {user.get('name', '')},\n\nYour new OTP is: {otp_code}\n\nGazarTech Team"
        )
        mail.send(msg)

        return jsonify({"message": "New OTP sent"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
