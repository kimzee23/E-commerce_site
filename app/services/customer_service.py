from flask import current_app
from werkzeug.security import generate_password_hash
from app.models.user_model import User


class CustomerService:
    @staticmethod
    def register_customer(name, email, password, role='customer'):
        mongo = current_app.mongo

        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            raise ValueError('Email already registered')

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role
        )

        result = mongo.db.users.insert_one(new_user.to_dict())
        return str(result.inserted_id)
