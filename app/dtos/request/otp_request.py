from pydantic import BaseModel, EmailStr, constr

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: constr(min_length=6, max_length=6, pattern=r'^\d{6}$')
