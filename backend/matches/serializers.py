from rest_framework import serializers

class CancelReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()