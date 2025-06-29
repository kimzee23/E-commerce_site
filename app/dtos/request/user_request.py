from pydantic import Field
from pydantic.v1 import BaseModel, EmailStr, validator

from app.enums.user_role import UserRole


class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str = Field(..., min_length=10, max_length=15)
    role: UserRole

    @validator("role")
    def validate_role(cls, role_value):
        allowed_roles = {"customer", "seller", "admin", "super_admin", "buyer"}
        if role_value not in allowed_roles:
            raise ValueError(f"Role must be one of: {', '.join(allowed_roles)}")
        return role_value

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)