from rest_framework import serializers

class TicketSearchSerializer(serializers.Serializer):
    sport_id = serializers.IntegerField(required=False)
    city_id = serializers.IntegerField(required=False)
    venue_id = serializers.IntegerField(required=False)
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    ticket_type_id = serializers.IntegerField(required=False)