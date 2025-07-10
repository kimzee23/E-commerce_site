from app.extentions import mongo

class OtpService:
    @staticmethod
    def verify(email: str, otp: str) -> str:
        user = mongo.db.users.find_one({"email": email})
        if not user:
            raise ValueError("User not found")

        if user.get("verified"):
            return "Already verified"

        if user.get("otp") == otp:
            mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"verified": True}})
            return "Email verified successfully"

        raise ValueError("Invalid OTP")
