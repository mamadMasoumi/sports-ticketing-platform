from rest_framework import serializers

class ReportSubmitSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField(required=False, allow_null=True)
    ticket_id = serializers.IntegerField(required=False, allow_null=True)
    category = serializers.CharField(max_length=100)
    description = serializers.CharField()