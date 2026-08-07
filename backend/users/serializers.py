import re
from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(min_length=8, write_only=True)
    city_id = serializers.IntegerField()
    birth_date = serializers.DateField(required=False, allow_null=True)

    def validate_phone(self, value):
        if not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError("Phone number must match the format 09XXXXXXXXX.")
        return value


class PasswordLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="Email or Phone number")
    password = serializers.CharField(write_only=True)


class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)

    def validate_phone(self, value):
        if not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError("Phone number must match the format 09XXXXXXXXX.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)

    def validate_phone(self, value):
        if not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError("Phone number must match the format 09XXXXXXXXX.")
        return value
