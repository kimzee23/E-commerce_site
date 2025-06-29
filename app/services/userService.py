from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app.enums.user_role import UserRole
from app.models.user_model import User
# from argon2

class UserService:
    @staticmethod
    def register(name, email, password, role, phone=None):
        mongo = current_app.mongo

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
        user = User(name=name, email=email, password=hashed_password, role=role, phone=phone)
        result = mongo.db.users.insert_one(user.to_dict())

        return str(result.inserted_id)

    @staticmethod
    def login(email, password, role):
        email = email.strip().lower()
        password = password.strip()
        print("LOGIN INPUTS:", email, password, role)
        if not email or not password:
            raise ValueError("Email and password cannot be empty.")
        mongo = current_app.mongo
        user = mongo.db.users.find_one({'email': email, 'role': role})
        print("FOUND USER:", user)
        if not user or not check_password_hash(user['password'], password):
            raise ValueError("Invalid credentials")

        return str(user['_id']), user
