import random
import redis
from django.conf import settings

# Initialize connection to the Redis container / instance
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class OTPService:
    """
    Handles OTP generation, temporary storage in Redis, and verification.
    """

    OTP_EXPIRY_SECONDS = 120  # OTP is valid for 2 minutes

    @staticmethod
    def generate_otp(phone: str) -> str:
        """
        Generates a 6-digit OTP code, stores it in Redis with a TTL, and returns it.
        """
        otp_code = f"{random.randint(100000, 999999)}"
        
        # Redis key format: 'otp:<phone_number>'
        key = f"otp:{phone}"
        redis_client.setex(key, OTPService.OTP_EXPIRY_SECONDS, otp_code)
        
        return otp_code

    @staticmethod
    def verify_otp(phone: str, submitted_code: str) -> bool:
        """
        Verifies the submitted OTP against the stored one in Redis.
        Removes the OTP key from Redis upon successful verification to prevent reuse.
        """
        key = f"otp:{phone}"
        stored_code = redis_client.get(key)
        
        if stored_code and stored_code == submitted_code:
            redis_client.delete(key)
            return True
            
        return False

