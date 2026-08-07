from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from tickets.serializers import TicketSearchSerializer
from tickets.services.ticket_search_service import TicketSearchService
from tickets.repositories.ticket_repository import TicketRepository

class TicketSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = TicketSearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Remove None values from filters
            filters = {k: v for k, v in serializer.validated_data.items() if v is not None}
            data = TicketSearchService.search(filters)
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TicketDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, ticket_id):
        try:
            ticket = TicketRepository.get_ticket_details(ticket_id)
            if ticket is None:
                return Response(
                    {"success": False, "error": "Ticket not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response({"success": True, "data": ticket}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )