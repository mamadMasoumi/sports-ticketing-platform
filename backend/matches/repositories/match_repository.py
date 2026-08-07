from django.db import connection

class MatchRepository:

    @staticmethod
    def list_matches():
        query = """
            SELECT
                m.id,
                m.match_date,
                m.status,
                s.name AS sport_name,
                v.name AS venue_name,
                t1.name AS home_team,
                t2.name AS away_team
            FROM Matches m
            JOIN Sports s ON m.sport_id = s.id
            JOIN Venues v ON m.venue_id = v.id
            JOIN Teams t1 ON m.home_team_id = t1.id
            JOIN Teams t2 ON m.away_team_id = t2.id
            ORDER BY m.match_date ASC
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            return [dict(zip(cols, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_match_by_id(match_id):
        query = """
            SELECT
                m.id,
                m.match_date,
                m.status,
                s.name AS sport_name,
                v.name AS venue_name,
                t1.name AS home_team,
                t2.name AS away_team
            FROM Matches m
            JOIN Sports s ON m.sport_id = s.id
            JOIN Venues v ON m.venue_id = v.id
            JOIN Teams t1 ON m.home_team_id = t1.id
            JOIN Teams t2 ON m.away_team_id = t2.id
            WHERE m.id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [match_id])
            row = cursor.fetchone()
            if not row:
                return None
            cols = [c[0] for c in cursor.description]
            return dict(zip(cols, row))
