import random

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.enums.user_role import UserRole
from app.models.user_model import User
from app import mongo

class UserService:
    @staticmethod
    def register(name, email, password, role, phone=None):
        name = name.strip()
        email = email.strip().lower()
        password = password.strip()

        if not name or not password:
            raise ValueError("Name and password cannot be empty or spaces only")

        if isinstance(role, UserRole):
            role = role.value

        if mongo.db.users.find_one({'email': email, 'role': role}):
            raise ValueError(f"{role.capitalize()} email already registered")

        if phone and mongo.db.users.find_one({'phone': phone, 'role': role}):
            raise ValueError(f"{role.capitalize()} phone already registered")

        hashed_password = generate_password_hash(password)

        otp = str(random.randint(100000, 999999))
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            phone=phone,
            is_active=True,
            otp=otp
        )

        result = mongo.db.users.insert_one(user.to_dict())


        return str(result.inserted_id), otp

    @staticmethod
    def login(email, password, role):
        email = email.strip().lower()
        password = password.strip()

        if not email or not password:
            raise ValueError("Email and password cannot be empty.")

        user = mongo.db.users.find_one({'email': email, 'role': role})

        if not user or not check_password_hash(user['password'], password):
            raise ValueError("Invalid credentials")

        return str(user['_id']), user
