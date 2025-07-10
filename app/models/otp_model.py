from datetime import datetime, timedelta, timezone
from bson import ObjectId

class OTP:
    def __init__(self, user_id, otp_code, created_at=None, expires_at=None, _id=None):
        self.id = _id
        self.user_id = ObjectId(user_id)
        self.otp_code = otp_code
        self.created_at = created_at or datetime.now(timezone.utc)
        self.expires_at = expires_at or (self.created_at + timedelta(minutes=10))

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "otp_code": self.otp_code,
            "created_at": self.created_at,
            "expires_at": self.expires_at
        }

    @staticmethod
    def from_dict(data):
        return OTP(
            user_id=data["user_id"],
            otp_code=data["otp_code"],
            created_at=data.get("created_at"),
            expires_at=data.get("expires_at"),
            _id=data.get("_id")
        )
