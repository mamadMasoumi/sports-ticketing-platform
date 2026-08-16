from django.db import connection
from reports.repositories.report_repository import ReportRepository

class ReportService:

    @staticmethod
    def submit_report(user_id, reservation_id, ticket_id, category, description):
        if not reservation_id and not ticket_id:
            raise ValueError("Either reservation_id or ticket_id must be provided.")

        if reservation_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM Reservations WHERE id = %s", [reservation_id])
                row = cursor.fetchone()
                if not row:
                    raise ValueError("Reservation not found.")
                if row[0] != user_id:
                    raise ValueError("This reservation does not belong to you.")

        if ticket_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM Tickets WHERE id = %s", [ticket_id])
                if not cursor.fetchone():
                    raise ValueError("Ticket not found.")

        report_id = ReportRepository.create_report(
            user_id=user_id,
            reservation_id=reservation_id,
            ticket_id=ticket_id,
            category=category,
            description=description
        )
        return {'report_id': report_id, 'status': 'Pending'}

    @staticmethod
    def review_report(report_id):
        report = ReportRepository.get_report_by_id(report_id)
        if not report:
            raise ValueError("Report not found.")
        ReportRepository.update_report_status(report_id, 'Reviewed')
        return ReportRepository.get_report_by_id(report_id)