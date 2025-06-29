from pydantic import BaseModel


class UserResponse(BaseModel):
    id : str
    name : str
    phone : str
    role : str