from datetime import datetime, timezone, timedelta
from app.extentions import mongo

class OtpService:
    @staticmethod
    def verify(email: str, otp: str) -> str:
        user = mongo.db.users.find_one({"email": email})
        if not user:
            raise ValueError("User not found")

        if user.get("verified"):
            return "Already verified"

        stored_otp = user.get("otp")
        otp_created_at = user.get("otp_created_at")

        if not stored_otp or not otp_created_at:
            raise ValueError("OTP not found or missing timestamp")

        # Check expiration (90 seconds)
        created_time = otp_created_at
        if isinstance(created_time, str):
            created_time = datetime.fromisoformat(created_time)
        if created_time.tzinfo is None:
            created_time = created_time.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        if now > created_time + timedelta(seconds=90):
            raise ValueError("Verification time passed. Click 'Resend OTP'.")

        if stored_otp != otp:
            raise ValueError("Invalid OTP")

        mongo.db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"verified": True}, "$unset": {"otp": "", "otp_created_at": ""}}
        )

        return "Email verified successfully"
