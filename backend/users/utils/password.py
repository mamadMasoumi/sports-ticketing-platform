from django.contrib.auth.hashers import make_password, check_password


class PasswordHasher:
    """
    Utility helper to securely hash and verify passwords using Django's built-in hashing system.
    """

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Hashes a plain-text password using the default Django hasher (PBKDF2 by default).
        """
        return make_password(plain_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain-text password against a hashed password.
        """
        return check_password(plain_password, hashed_password)
