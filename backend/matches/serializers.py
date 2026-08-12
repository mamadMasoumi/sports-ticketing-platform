from rest_framework import serializers


class ReserveTicketSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(min_value=1)


class CancelReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField(min_value=1)
