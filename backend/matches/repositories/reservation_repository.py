from django.db import connection

class ReservationRepository:
    """
    Raw SQL helpers for the Reservations table.
    """

    @staticmethod
    def get_reservation_for_cancel(cursor, reservation_id):
        """
        Lock the reservation and join Tickets + Matches to get
        ticket price and match date. Used in cancellation flow.
        """
        query = """
            SELECT r.id, r.user_id, r.ticket_id, r.status, r.expire_time,
                   t.price, m.match_date
            FROM Reservations r
            JOIN Tickets t ON r.ticket_id = t.id
            JOIN Matches m ON t.match_id = m.id
            WHERE r.id = %s
            FOR UPDATE
        """
        cursor.execute(query, [reservation_id])
        return cursor.fetchone()

    @staticmethod
    def restore_ticket_capacity(cursor, ticket_id):
        """Increment remaining_capacity for a ticket by 1."""
        cursor.execute(
            "UPDATE Tickets SET remaining_capacity = remaining_capacity + 1 "
            "WHERE id = %s",
            [ticket_id]
        )

    @staticmethod
    def update_reservation_status(cursor, reservation_id, new_status):
        """Set the reservation status (e.g., 'Canceled')."""
        cursor.execute(
            "UPDATE Reservations SET status = %s WHERE id = %s",
            [new_status, reservation_id]
        )