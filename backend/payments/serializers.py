from rest_framework import serializers

# Enum values from your DB: 'BankCard', 'Wallet', 'Crypto'
PAYMENT_METHOD_CHOICES = ('BankCard', 'Wallet', 'Crypto')

class PayReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=PAYMENT_METHOD_CHOICES)