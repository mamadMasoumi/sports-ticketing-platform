from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import (
    UserRegisterSerializer,
    PasswordLoginSerializer,
    RequestOTPSerializer,
    VerifyOTPSerializer,
    UserUpdateSerializer
)
from users.services.auth_service import AuthService, ProfileService
from users.services.otp_service import OTPService, RateLimitError
from users.repositories.user_repository import UserRepository


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_id = AuthService.register_user(
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'],
                    phone=serializer.validated_data['phone'],
                    password=serializer.validated_data['password'],
                    city_id=serializer.validated_data['city_id'],
                    birth_date=serializer.validated_data.get('birth_date')
                )
                return Response({"message": "User registered successfully", "user_id": user_id}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = AuthService.authenticate_by_password(
                    identifier=serializer.validated_data['identifier'],
                    password=serializer.validated_data['password']
                )
                return Response(result, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            user_record = UserRepository.get_user_by_phone(phone)
            if not user_record:
                return Response({"error": "User with this phone number not found."}, status=status.HTTP_404_NOT_FOUND)
            try:
                otp_code = OTPService.generate_otp(phone)
                return Response({"message": "OTP sent successfully", "code_dev_only": otp_code}, status=status.HTTP_200_OK)
            except RateLimitError as e:
                return Response({"error": str(e)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            try:
                if not OTPService.verify_otp(phone, code):
                    return Response({"error": "Invalid or expired OTP code."}, status=status.HTTP_400_BAD_REQUEST)
            except RateLimitError as e:
                return Response({"error": str(e)}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            user_record = UserRepository.get_user_by_phone(phone)
            if not user_record:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            user_id = user_record[0]
            user_role = user_record[6]
            token = AuthService.generate_jwt_token(user_id, user_role)
            return Response({
                'token': token,
                'user': {
                    'id': user_id,
                    'first_name': user_record[1],
                    'last_name': user_record[2],
                    'email': user_record[3],
                    'role': user_role
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                updated_data = ProfileService.update_profile(
                    user_id=request.user.id,
                    **serializer.validated_data
                )
                return Response({"success": True, "data": updated_data}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)