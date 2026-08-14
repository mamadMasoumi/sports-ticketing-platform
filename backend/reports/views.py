from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, date
from decimal import Decimal

from reports.serializers import ReportSubmitSerializer
from reports.services.report_service import ReportService
from reports.repositories.report_repository import ReportRepository
from users.utils.permissions import is_support_or_admin

class SubmitReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            result = ReportService.submit_report(
                user_id=request.user.id,
                reservation_id=serializer.validated_data.get('reservation_id'),
                ticket_id=serializer.validated_data.get('ticket_id'),
                category=serializer.validated_data['category'],
                description=serializer.validated_data['description']
            )
            return Response(
                {"success": True, "data": result},
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


class UserReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            rows = ReportRepository.get_reports_by_user(request.user.id)
            # Serialize datetime fields
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, (datetime, date)):
                        row[key] = value.isoformat()
                    elif isinstance(value, Decimal):
                        row[key] = float(value)
            return Response(
                {"success": True, "data": rows},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AllReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not is_support_or_admin(request.user):
            return Response({"success": False, "error": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        status_filter = request.query_params.get('status_filter')
        if status_filter is not None and status_filter not in ('Pending', 'Reviewed'):
            return Response({"success": False, "error": "Invalid status_filter value."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rows = ReportRepository.get_all_reports(status_filter=status_filter)
            for row in rows:
                # create_at may be a datetime
                if 'created_at' in row and isinstance(row['created_at'], (datetime, date)):
                    row['created_at'] = row['created_at'].isoformat()
            return Response({"success": True, "data": rows}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, report_id):
        if not is_support_or_admin(request.user):
            return Response({"success": False, "error": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        try:
            updated_report = ReportService.review_report(report_id)
            return Response({"success": True, "data": updated_report}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)