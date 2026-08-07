from django.db import connection, transaction
from django.utils import timezone
from datetime import timedelta

class ReservationService:
    @staticmethod
    def reserve_ticket(user_id, ticket_id):
        """
        Reserve a ticket. Checks capacity and creates a reservation with a
        10-minute expiry.
        """
        with transaction.atomic():
            with connection.cursor() as cursor:
                # 1. Lock the ticket row and get its remaining capacity
                cursor.execute(
                    "SELECT id, remaining_capacity FROM Tickets WHERE id = %s FOR UPDATE",
                    [ticket_id]
                )
                ticket = cursor.fetchone()
                if not ticket:
                    raise ValueError("Ticket not found.")
                if ticket[1] <= 0:
                    raise ValueError("No tickets left.")

                # 2. Check if user already has an active (unexpired) reservation for this ticket
                #    to prevent double booking (optional, can be removed)
                cursor.execute(
                    """SELECT id FROM Reservations
                       WHERE user_id = %s AND ticket_id = %s
                         AND status = 'Reserved' AND expire_time > %s
                       LIMIT 1""",
                    [user_id, ticket_id, timezone.now()]
                )
                if cursor.fetchone():
                    raise ValueError("You already have an active reservation for this ticket.")

                # 3. Decrement capacity
                cursor.execute(
                    "UPDATE Tickets SET remaining_capacity = remaining_capacity - 1 WHERE id = %s",
                    [ticket_id]
                )

                # 4. Create reservation with expire_time = now + 10 minutes
                expire_time = timezone.now() + timedelta(minutes=10)
                cursor.execute(
                    """INSERT INTO Reservations (user_id, ticket_id, status, reserve_time, expire_time)
                       VALUES (%s, %s, 'Reserved', %s, %s)""",
                    [user_id, ticket_id, timezone.now(), expire_time]
                )

                return cursor.lastrowid