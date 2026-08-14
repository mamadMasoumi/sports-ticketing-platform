import random
import redis
from django.conf import settings

# Initialize connection to the Redis container / instance
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class RateLimitError(Exception):
    """Raised when a user exceeds the allowed number of OTP requests or verification attempts."""
    pass


class OTPService:
    """
    Handles OTP generation, temporary storage in Redis, and verification.
    Also enforces rate limits on request and verification attempts.
    """

    OTP_EXPIRY_SECONDS = 120          # OTP is valid for 2 minutes
    REQUEST_LIMIT = 3                 # max OTP requests per phone in window
    REQUEST_WINDOW_SECONDS = 600      # 10 minutes
    VERIFY_LIMIT = 5                  # max failed verification attempts per phone
    VERIFY_WINDOW_SECONDS = 600       # 10 minutes

    @staticmethod
    def generate_otp(phone: str) -> str:
        """
        Generates a 6-digit OTP code, stores it in Redis with a TTL, and returns it.
        Enforces a request rate limit (max 3 requests per 10 minutes per phone).
        """
        request_key = f"otp_request_count:{phone}"

        # Increment request counter; if this is the first increment, set expiry window
        count = redis_client.incr(request_key)
        if count == 1:
            redis_client.expire(request_key, OTPService.REQUEST_WINDOW_SECONDS)

        if count > OTPService.REQUEST_LIMIT:
            raise RateLimitError(
                "Too many OTP requests. Please try again later."
            )

        # Generate OTP and store with expiry
        otp_code = f"{random.randint(100000, 999999)}"
        key = f"otp:{phone}"
        redis_client.setex(key, OTPService.OTP_EXPIRY_SECONDS, otp_code)
        return otp_code

    @staticmethod
    def verify_otp(phone: str, submitted_code: str) -> bool:
        """
        Verifies the submitted OTP against the stored one in Redis.
        Tracks failed attempts and locks out after exceeding the limit.
        Removes the OTP key and failure counter upon successful verification.
        """
        fail_key = f"otp_fail_count:{phone}"

        # Check if already locked out
        fail_count = redis_client.get(fail_key)
        if fail_count is not None and int(fail_count) >= OTPService.VERIFY_LIMIT:
            raise RateLimitError(
                "Too many failed OTP verification attempts. Please try again later."
            )

        key = f"otp:{phone}"
        stored_code = redis_client.get(key)

        if stored_code and stored_code == submitted_code:
            # Success: delete OTP and failure counter
            redis_client.delete(key)
            redis_client.delete(fail_key)
            return True

        # Failure: increment fail counter
        new_fail_count = redis_client.incr(fail_key)
        if new_fail_count == 1:
            redis_client.expire(fail_key, OTPService.VERIFY_WINDOW_SECONDS)

        return False