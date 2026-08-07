from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .repositories.match_repository import MatchRepository
from .services.reservation_service import ReservationService


class MatchListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            data = MatchRepository.list_matches()
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MatchDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, match_id):
        try:
            match = MatchRepository.get_match_by_id(match_id)
            if not match:
                return Response({"success": False, "error": "Match not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"success": True, "data": match}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReserveTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user["id"]
        match_id = request.data.get("match_id")
        seat_number = request.data.get("seat_number")
        ticket_type_id = request.data.get("ticket_type_id")

        if not all([match_id, seat_number, ticket_type_id]):
            return Response(
                {"success": False, "error": "match_id, seat_number, ticket_type_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reservation_id = ReservationService.reserve_ticket(
                user_id, match_id, seat_number, ticket_type_id
            )
            return Response(
                {"success": True, "reservation_id": reservation_id},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
