from datetime import datetime
from werkzeug.security import generate_password_hash
class User:
    def __init__(self, name, email, password, role="customer", is_active=True, created_at=None, phone=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.phone = phone


    def _hash_password(self, plain_password):
        return generate_password_hash(plain_password)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "phone": self.phone
        }

    @staticmethod
    def from_dict(data):
        return User(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role", "customer"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            phone=data.get("phone"),
            is_hashed=True
        )
