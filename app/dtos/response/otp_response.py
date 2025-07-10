from pydantic import BaseModel
from typing import Optional

class OtpVerificationResponse(BaseModel):
    message: str
    success: bool
    user_id: Optional[str] = None