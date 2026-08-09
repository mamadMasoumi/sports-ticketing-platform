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


    @staticmethod
    def get_user_reservations(user_id, status_filter=None):
        """
        Returns all reservations for a user with full context:
        ticket price/type, match date/status, sport, venue, teams,
        and the latest payment (if any).
        """
        base_query = """
                SELECT r.id AS reservation_id,
                       r.status,
                       r.reserve_time,
                       r.expire_time,
                       t.price AS ticket_price,
                       tt.type_name AS ticket_type,
                       m.match_date,
                       m.status AS match_status,
                       s.sport_name,
                       v.venue_name,
                       home.team_name AS home_team,
                       away.team_name AS away_team,
                       p.payment_status,
                       p.amount AS payment_amount,
                       p.payment_method
                FROM Reservations r
                JOIN Tickets t ON r.ticket_id = t.id
                JOIN TicketTypes tt ON t.ticket_type_id = tt.id
                JOIN Matches m ON t.match_id = m.id
                JOIN Sports s ON m.sport_id = s.id
                JOIN Venues v ON m.venue_id = v.id
                JOIN Teams home ON m.home_team_id = home.id
                JOIN Teams away ON m.away_team_id = away.id
                LEFT JOIN Payments p ON p.reservation_id = r.id
                    AND p.id = (
                        SELECT MAX(p2.id) FROM Payments p2
                        WHERE p2.reservation_id = r.id
                    )
                WHERE r.user_id = %s
            """
        params = [user_id]

        if status_filter:
            base_query += " AND r.status = %s"
            params.append(status_filter)

        base_query += " ORDER BY r.reserve_time DESC"

        with connection.cursor() as cursor:
            cursor.execute(base_query, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]
