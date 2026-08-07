from django.db import connection, transaction

class ReservationService:

    @staticmethod
    def reserve_ticket(user_id, match_id, seat_number, ticket_type_id):
        with transaction.atomic():
            with connection.cursor() as cursor:
                check_query = """
                    SELECT id
                    FROM Reservations
                    WHERE match_id = %s AND seat_number = %s
                    FOR UPDATE
                """
                cursor.execute(check_query, [match_id, seat_number])
                if cursor.fetchone():
                    raise ValueError("این صندلی قبلاً رزرو شده است.")

                insert_query = """
                    INSERT INTO Reservations
                    (user_id, match_id, seat_number, ticket_type_id, status, reserved_at)
                    VALUES (%s, %s, %s, %s, 'pending', NOW())
                """
                cursor.execute(insert_query, [user_id, match_id, seat_number, ticket_type_id])
                return cursor.lastrowid
