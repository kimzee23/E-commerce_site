import random
from werkzeug.security import generate_password_hash, check_password_hash
from app.enums.user_role import UserRole
from app.models.user_model import User
from app.extentions import mongo

class UserService:
    @staticmethod
    def register(name, email, password, role, phone=None):
        print("🐞 Entered UserService.register()")

        # Normalize and validate inputs
        name = name.strip()
        email = email.strip().lower()
        password = password.strip()

        print("📩 Registration Details:")
        print(f" - Name: {name}")
        print(f" - Email: {email}")
        print(f" - Role: {role}")
        print(f" - Phone: {phone}")

        # Basic validations
        if not name or not password:
            raise ValueError("Name and password cannot be empty or spaces only")

        # Ensure role is string value
        if isinstance(role, UserRole):
            role = role.value

        # Check for existing user with same email and role
        print("🔍 Checking for existing email+role match...")
        existing_email_user = mongo.db.users.find_one({'email': email, 'role': role})
        print("   ➤ Found by email+role:", existing_email_user)

        if existing_email_user and "_id" in existing_email_user:
            raise ValueError(f"{role.capitalize()} email already registered")

        # Optional: Check for duplicate phone for same role
        if phone:
            print("🔍 Checking for existing phone+role match...")
            existing_phone_user = mongo.db.users.find_one({'phone': phone, 'role': role})
            print("   ➤ Found by phone+role:", existing_phone_user)

            if existing_phone_user and "_id" in existing_phone_user:
                raise ValueError(f"{role.capitalize()} phone already registered")

        # All good — hash password & generate OTP
        hashed_password = generate_password_hash(password)
        otp = str(random.randint(100000, 999999))

        # Create User model and save
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            phone=phone,
            is_active=True,
            otp=otp
        )

        print("💾 Saving new user to MongoDB...")
        result = mongo.db.users.insert_one(user.to_dict())
        print(f"✅ User inserted with ID: {result.inserted_id}")

        # Return ID and OTP for email verification
        return str(result.inserted_id), otp

        @staticmethod
        def login(email, password, role):
            email = email.strip().lower()
            password = password.strip()

            if not email or not password:
                raise ValueError("Email and password cannot be empty.")

            print(f" Login attempt: email={email}, role={role}")
            user = mongo.db.users.find_one({'email': email, 'role': role})
            print(f" - User found: {user}")

            if not user or not check_password_hash(user['password'], password):
                raise ValueError("Invalid credentials")

            return str(user['_id']), user
