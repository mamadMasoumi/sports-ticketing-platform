from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.services.auth_service import AuthService
from users.repositories.user_repository import UserRepository


class AuthenticatedUser:
    """
    A lightweight, non-ORM user class to represent the logged-in user in request.user
    """
    def __init__(self, user_id, role, email, first_name, last_name):
        self.id = user_id
        self.role = role
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_authenticated = True


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication class using raw SQL user fetching.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None

        token = parts[1]
        payload = AuthService.verify_jwt_token(token)
        if not payload:
            raise AuthenticationFailed('Invalid or expired token.')

        user_id = payload.get('user_id')
        user_record = UserRepository.get_user_by_id(user_id)

        if not user_record:
            raise AuthenticationFailed('User not found.')

        # Tuple structure matching database output:
        # (id, first_name, last_name, email, phone, password, role, city_id, birth_date, profile_image, status, ...)
        status = user_record[10]
        if status != 'active':
            raise AuthenticationFailed('User account is inactive or suspended.')

        user = AuthenticatedUser(
            user_id=user_record[0],
            role=user_record[6],
            email=user_record[3],
            first_name=user_record[1],
            last_name=user_record[2]
        )

        return (user, token)
