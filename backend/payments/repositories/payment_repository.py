from django.db import connection
from django.utils import timezone
import uuid

class PaymentRepository:
    @staticmethod
    def create_payment(reservation_id, user_id, amount, method, status='Pending',
                       transaction_code=None):
        query = """
            INSERT INTO Payments (reservation_id, user_id, amount,
                                   payment_method, payment_status,
                                   payment_time, transaction_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        now = timezone.now()
        payment_time = now if status == 'Success' else None
        if not transaction_code:
            transaction_code = None   # keep as NULL
        with connection.cursor() as cursor:
            cursor.execute(query, [
                reservation_id, user_id, amount, method, status,
                payment_time, transaction_code
            ])
            return cursor.lastrowid

    @staticmethod
    def get_payment_by_reservation(reservation_id):
        query = """
            SELECT id, reservation_id, user_id, amount,
                   payment_method, payment_status, payment_time, transaction_code
            FROM Payments
            WHERE reservation_id = %s
            ORDER BY id DESC
            LIMIT 1
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [reservation_id])
            return cursor.fetchone()

    @staticmethod
    def get_payment_by_id(payment_id):
        query = """
            SELECT id, reservation_id, user_id, amount,
                   payment_method, payment_status, payment_time, transaction_code
            FROM Payments
            WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [payment_id])
            return cursor.fetchone()

    @staticmethod
    def update_payment_status(payment_id, status, transaction_code=None):
        query = """
            UPDATE Payments
            SET payment_status = %s,
                payment_time = %s,
                transaction_code = %s
            WHERE id = %s
        """
        payment_time = timezone.now() if status == 'Success' else None
        with connection.cursor() as cursor:
            cursor.execute(query, [status, payment_time, transaction_code, payment_id])
            return cursor.rowcount

    @staticmethod
    def list_payments_by_user(user_id, limit=50, offset=0):
        query = """
            SELECT id, reservation_id, user_id, amount,
                   payment_method, payment_status, payment_time, transaction_code
            FROM Payments
            WHERE user_id = %s
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id, limit, offset])
            return cursor.fetchall()