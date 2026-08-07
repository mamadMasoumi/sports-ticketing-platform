import jwt
from datetime import datetime, timedelta
from django.conf import settings
from users.repositories.user_repository import UserRepository
from users.utils.password import PasswordHasher


class AuthService:
    """
    Service layer executing high-level business logic for registration and session tokens.
    """

    JWT_SECRET = settings.SECRET_KEY
    JWT_ALGORITHM = 'HS256'
    TOKEN_EXPIRY_HOURS = 24

    @staticmethod
    def generate_jwt_token(user_id: int, role: str) -> str:
        """
        Generates a JWT token for the authenticated user.
        """
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=AuthService.TOKEN_EXPIRY_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, AuthService.JWT_SECRET, algorithm=AuthService.JWT_ALGORITHM)

    @staticmethod
    def verify_jwt_token(token: str) -> dict:
        """
        Verifies and decodes a JWT token. Returns payload dict or None if invalid.
        """
        try:
            payload = jwt.decode(token, AuthService.JWT_SECRET, algorithms=[AuthService.JWT_ALGORITHM])
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @classmethod
    def register_user(cls, first_name, last_name, email, phone, password, city_id, birth_date=None):
        """
        Handles user registration business requirements: checking duplicates, hashing passwords,
        and executing Raw SQL write through the UserRepository.
        """
        # 1. Check if user already exists
        if UserRepository.get_user_by_email(email):
            raise ValueError("User with this email already exists.")
            
        if UserRepository.get_user_by_phone(phone):
            raise ValueError("User with this phone number already exists.")

        # 2. Hash password
        hashed_password = PasswordHasher.hash_password(password)

        # 3. Create via repository
        user_id = UserRepository.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=hashed_password,
            city_id=city_id,
            birth_date=birth_date
        )
        return user_id

    @classmethod
    def authenticate_by_password(cls, identifier: str, password: str) -> dict:
        """
        Authenticates a user via email or phone. Returns JWT token and basic user info.
        """
        # Check both email and phone
        user_record = UserRepository.get_user_by_email(identifier)
        if not user_record:
            user_record = UserRepository.get_user_by_phone(identifier)

        if not user_record:
            raise ValueError("Invalid credentials.")

        # Mapping the database result tuple:
        # (id, first_name, last_name, email, phone, password, role, city_id, birth_date, profile_image, status, ...)
        db_password = user_record[5]
        user_status = user_record[10]

        if user_status != 'active':
            raise ValueError("This account is not active.")

        # Verify hashed password
        if not PasswordHasher.verify_password(password, db_password):
            raise ValueError("Invalid credentials.")

        # Generate JWT Token
        user_id = user_record[0]
        user_role = user_record[6]
        token = cls.generate_jwt_token(user_id, user_role)

        return {
            'token': token,
            'user': {
                'id': user_id,
                'first_name': user_record[1],
                'last_name': user_record[2],
                'email': user_record[3],
                'role': user_role
            }
        }
