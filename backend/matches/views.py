from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime, date
from decimal import Decimal

from .repositories.match_repository import MatchRepository
from .repositories.reservation_repository import ReservationRepository  # <-- new import
from .services.reservation_service import ReservationService
from matches.services.reservation_cancellation_service import ReservationCancellationService
from matches.serializers import CancelReservationSerializer
from users.utils.permissions import is_support_or_admin

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
        ticket_id = request.data.get("ticket_id")
        if not ticket_id:
            return Response(
                {"success": False, "error": "ticket_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            reservation_id = ReservationService.reserve_ticket(
                user_id=request.user.id,
                ticket_id=ticket_id
            )
            return Response(
                {"success": True, "reservation_id": reservation_id},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CancelReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CancelReservationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            result = ReservationCancellationService.cancel_reservation(
                user_id=request.user.id,
                reservation_id=serializer.validated_data['reservation_id']
            )
            return Response(
                {"success": True, "data": result},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get('status_filter')
        # Basic validation
        if status_filter and status_filter not in ('Reserved', 'Paid', 'Canceled', 'Expired'):
            return Response(
                {"success": False, "error": "Invalid status_filter value."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            rows = ReservationRepository.get_user_reservations(
                user_id=request.user.id,
                status_filter=status_filter
            )
            # Serialise datetime/Decimal for JSON output
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, (datetime, date)):
                        row[key] = value.isoformat()
                    elif isinstance(value, Decimal):
                        row[key] = float(value)

            return Response({"success": True, "data": rows}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminCancelReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        if not is_support_or_admin(request.user):
            return Response({"success": False, "error": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        try:
            result = ReservationCancellationService.admin_cancel_reservation(
                reservation_id=reservation_id,
                admin_user_id=request.user.id
            )
            return Response({"success": True, "data": result}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)