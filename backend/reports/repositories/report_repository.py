from django.db import connection
from django.utils import timezone

class ReportRepository:

    @staticmethod
    def create_report(user_id, reservation_id, ticket_id, category, description):
        query = """
            INSERT INTO Reports (user_id, reservation_id, ticket_id, category, description, status, created_at)
            VALUES (%s, %s, %s, %s, %s, 'Pending', %s)
        """
        now = timezone.now()
        with connection.cursor() as cursor:
            cursor.execute(query, [
                user_id,
                reservation_id,
                ticket_id,
                category,
                description,
                now
            ])
            return cursor.lastrowid

    @staticmethod
    def get_reports_by_user(user_id):
        query = """
            SELECT id, user_id, reservation_id, ticket_id, category, description, status, created_at
            FROM Reports
            WHERE user_id = %s
            ORDER BY created_at DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(cols, row)) for row in rows]

    @staticmethod
    def get_report_by_id(report_id):
        query = """
            SELECT id, user_id, reservation_id, ticket_id, category, description, status, created_at
            FROM Reports
            WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [report_id])
            row = cursor.fetchone()
            if not row:
                return None
            cols = [c[0] for c in cursor.description]
            return dict(zip(cols, row))