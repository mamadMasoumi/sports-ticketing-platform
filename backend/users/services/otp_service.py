import random
import redis
from django.conf import settings

# Initialize Redis client connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class OTPService:
    @staticmethod
    def generate_otp(phone_number: str) -> str:
        """
        Generates a 6-digit verification code, stores it in Redis with 
        a 120-second expiration time, and prepares it for sending.
        """
        otp_code = str(random.randint(100000, 999999))
        redis_client.setex(f"otp:{phone_number}", 120, otp_code)
        
        # Logging dynamic OTP code for local debugging environments
        print(f"[DEBUG] OTP generated for {phone_number}: {otp_code}")
        return otp_code

    @staticmethod
    def verify_otp(phone_number: str, code: str) -> bool:
        """
        Verifies the provided OTP code against the Redis value.
        Deletes the OTP code immediately upon successful validation to prevent reuse.
        """
        stored_code = redis_client.get(f"otp:{phone_number}")
        if stored_code and stored_code == code:
            redis_client.delete(f"otp:{phone_number}")
            return True
        return False
