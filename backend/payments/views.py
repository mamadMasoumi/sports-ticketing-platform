from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from payments.serializers import PayReservationSerializer
from payments.services.payment_service import PaymentService
from payments.repositories.payment_repository import PaymentRepository

class PayForReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PayReservationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = PaymentService.pay_for_reservation(
                user_id=request.user.id,
                reservation_id=serializer.validated_data['reservation_id'],
                method=serializer.validated_data['method'],
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

class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reservation_id):
        row = PaymentRepository.get_payment_by_reservation(reservation_id)
        if not row:
            return Response(
                {"success": False, "error": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # row[2] is user_id
        if row[2] != request.user.id:
            return Response(
                {"success": False, "error": "Not authorized."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = {
            'id': row[0],
            'reservation_id': row[1],
            'user_id': row[2],
            'amount': str(row[3]),
            'payment_method': row[4],
            'payment_status': row[5],
            'payment_time': row[6],
            'transaction_code': row[7],
        }
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)