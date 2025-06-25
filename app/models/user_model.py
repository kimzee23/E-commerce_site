from datetime import datetime
from werkzeug.security import generate_password_hash

class User:
    def __init__(self, name, email, password, role="customer", is_active=True, created_at=None):
        self.name = name
        self.email = email
        self.password = self._hash_password(password)
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()

    def _hash_password(self, plain_password):
        return generate_password_hash(plain_password)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data):
        return User(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),  # already hashed if reading from DB
            role=data.get("role", "customer"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at")
        )
