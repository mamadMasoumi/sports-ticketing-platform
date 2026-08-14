from django.db import connection


class LocationRepository:

    @staticmethod
    def get_all_cities():
        query = """
            SELECT id, province, city_name
            FROM Cities
            ORDER BY province, city_name
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(cols, row)) for row in rows]

    @staticmethod
    def get_all_venues(city_id=None):
        query = """
            SELECT id, venue_name, city_id, address, capacity
            FROM Venues
        """
        params = []

        if city_id is not None:
            query += " WHERE city_id = %s"
            params.append(city_id)

        query += " ORDER BY venue_name"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(cols, row)) for row in rows]