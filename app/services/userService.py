from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import User
# from argon2

class UserService:
    @staticmethod
    def register(name, email, password, role, phone=None):
        mongo = current_app.mongo
        if mongo.db.users.find_one({'email': email, 'role': role}):
            raise ValueError(f"{role.capitalize}Email already registered")

        if mongo.db.users.find_one({'phone': phone, 'role': role}):
            raise ValueError(f"{role.capitalize}Phone already registered")


        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password, role=role, phone=phone)
        result = mongo.db.users.insert_one(user.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def login(email, password, role):
        mongo = current_app.mongo
        user = mongo.db.users.find_one({'email': email, 'role': role})
        if not user or not check_password_hash(user['password'], password):
            raise ValueError('invalid credentials')
        return str(user['_id']), user
