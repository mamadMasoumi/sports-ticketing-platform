from django.db import connection

class TicketRepository:
    @staticmethod
    def search_tickets(filters: dict):
        """
        Build dynamic SQL to search available tickets.
        filters can contain:
          sport_id, city_id, venue_id, date_from, date_to,
          min_price, max_price, ticket_type_id
        Only returns tickets with remaining_capacity > 0 and match status = 'Scheduled'.
        Ordered by match_date ASC.
        Returns a list of dicts.
        """
        base_query = """
            SELECT
                t.id AS ticket_id,
                t.price,
                t.remaining_capacity,
                tt.type_name AS ticket_type,
                m.id AS match_id,
                m.match_date,
                s.sport_name,
                v.venue_name,
                v.address AS venue_address,
                c.city_name AS venue_city,
                c.id AS city_id,
                home.team_name AS home_team,
                away.team_name AS away_team
            FROM Tickets t
            JOIN TicketTypes tt ON t.ticket_type_id = tt.id
            JOIN Matches m ON t.match_id = m.id
            JOIN Sports s ON m.sport_id = s.id
            JOIN Venues v ON m.venue_id = v.id
            JOIN Cities c ON v.city_id = c.id
            JOIN Teams home ON m.home_team_id = home.id
            JOIN Teams away ON m.away_team_id = away.id
            WHERE t.remaining_capacity > 0
              AND m.status = 'Scheduled'
        """
        conditions = []
        params = []

        if filters.get('sport_id') is not None:
            conditions.append("s.id = %s")
            params.append(filters['sport_id'])

        if filters.get('city_id') is not None:
            conditions.append("c.id = %s")
            params.append(filters['city_id'])

        if filters.get('venue_id') is not None:
            conditions.append("v.id = %s")
            params.append(filters['venue_id'])

        if filters.get('date_from') is not None:
            conditions.append("m.match_date >= %s")
            params.append(filters['date_from'])

        if filters.get('date_to') is not None:
            conditions.append("m.match_date <= %s")
            params.append(filters['date_to'])

        if filters.get('min_price') is not None:
            conditions.append("t.price >= %s")
            params.append(filters['min_price'])

        if filters.get('max_price') is not None:
            conditions.append("t.price <= %s")
            params.append(filters['max_price'])

        if filters.get('ticket_type_id') is not None:
            conditions.append("tt.id = %s")
            params.append(filters['ticket_type_id'])

        if conditions:
            base_query += " AND " + " AND ".join(conditions)

        base_query += " ORDER BY m.match_date ASC"

        with connection.cursor() as cursor:
            cursor.execute(base_query, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_ticket_details(ticket_id):
        """
        Full ticket details with sport-specific information.
        """
        # Main ticket + match info
        base_query = """
            SELECT
                t.id AS ticket_id,
                t.price,
                t.remaining_capacity,
                tt.type_name AS ticket_type,
                m.id AS match_id,
                m.match_date,
                m.status AS match_status,
                s.sport_name,
                s.id AS sport_id,
                v.venue_name,
                v.address AS venue_address,
                c.city_name AS venue_city,
                home.team_name AS home_team,
                away.team_name AS away_team
            FROM Tickets t
            JOIN TicketTypes tt ON t.ticket_type_id = tt.id
            JOIN Matches m ON t.match_id = m.id
            JOIN Sports s ON m.sport_id = s.id
            JOIN Venues v ON m.venue_id = v.id
            JOIN Cities c ON v.city_id = c.id
            JOIN Teams home ON m.home_team_id = home.id
            JOIN Teams away ON m.away_team_id = away.id
            WHERE t.id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(base_query, [ticket_id])
            row = cursor.fetchone()
            if not row:
                return None
            columns = [col[0] for col in cursor.description]
            ticket = dict(zip(columns, row))

            # Determine sport and fetch sport-specific details
            sport_name = ticket['sport_name']
            extra = None
            if sport_name == 'Football':
                cursor.execute(
                    "SELECT league, seat, seat_row, parking, roof, vip_service "
                    "FROM FootballDetails WHERE ticket_id = %s",
                    [ticket_id]
                )
                extra_row = cursor.fetchone()
                if extra_row:
                    extra = {
                        'league': extra_row[0],
                        'seat': extra_row[1],
                        'seat_row': extra_row[2],
                        'parking': bool(extra_row[3]),
                        'roof': bool(extra_row[4]),
                        'vip_service': bool(extra_row[5]),
                    }
            elif sport_name == 'Basketball':
                cursor.execute(
                    "SELECT league, seat, seat_row, vip_service "
                    "FROM BasketballDetails WHERE ticket_id = %s",
                    [ticket_id]
                )
                extra_row = cursor.fetchone()
                if extra_row:
                    extra = {
                        'league': extra_row[0],
                        'seat': extra_row[1],
                        'seat_row': extra_row[2],
                        'vip_service': bool(extra_row[3]),
                    }
            elif sport_name == 'Volleyball':
                cursor.execute(
                    "SELECT league, seat, seat_row, special_service "
                    "FROM VolleyballDetails WHERE ticket_id = %s",
                    [ticket_id]
                )
                extra_row = cursor.fetchone()
                if extra_row:
                    extra = {
                        'league': extra_row[0],
                        'seat': extra_row[1],
                        'seat_row': extra_row[2],
                        'special_service': bool(extra_row[3]),
                    }

            ticket['details'] = extra
            return ticket