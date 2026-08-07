from django.db import connection
from django.utils import timezone


class UserRepository:
    """
    Repository for direct raw SQL access to the Users table.
    """

    @staticmethod
    def create_user(first_name, last_name, email, phone, password,
                    city_id, role='user', birth_date=None, profile_image=None,
                    status='active'):
        query = """
            INSERT INTO Users
            (first_name, last_name, email, phone, password, role, city_id,
             birth_date, profile_image, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        now = timezone.now()

        with connection.cursor() as cursor:
            cursor.execute(
                query,
                [
                    first_name,
                    last_name,
                    email,
                    phone,
                    password,
                    role,
                    city_id,
                    birth_date,
                    profile_image,
                    status,
                    now,
                    now,
                ],
            )
            return cursor.lastrowid

    @staticmethod
    def get_user_by_id(user_id):
        query = """
            SELECT id, first_name, last_name, email, phone, password, role,
                   city_id, birth_date, profile_image, status,
                   created_at, updated_at
            FROM Users
            WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            row = cursor.fetchone()
            return row

    @staticmethod
    def get_user_by_email(email):
        query = """
            SELECT id, first_name, last_name, email, phone, password, role,
                   city_id, birth_date, profile_image, status,
                   created_at, updated_at
            FROM Users
            WHERE email = %s
            LIMIT 1
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [email])
            return cursor.fetchone()

    @staticmethod
    def get_user_by_phone(phone):
        query = """
            SELECT id, first_name, last_name, email, phone, password, role,
                   city_id, birth_date, profile_image, status,
                   created_at, updated_at
            FROM Users
            WHERE phone = %s
            LIMIT 1
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [phone])
            return cursor.fetchone()

    @staticmethod
    def update_user(user_id, first_name=None, last_name=None, email=None,
                    phone=None, password=None, city_id=None, role=None,
                    birth_date=None, profile_image=None, status=None):
        fields = []
        values = []

        if first_name is not None:
            fields.append("first_name = %s")
            values.append(first_name)
        if last_name is not None:
            fields.append("last_name = %s")
            values.append(last_name)
        if email is not None:
            fields.append("email = %s")
            values.append(email)
        if phone is not None:
            fields.append("phone = %s")
            values.append(phone)
        if password is not None:
            fields.append("password = %s")
            values.append(password)
        if city_id is not None:
            fields.append("city_id = %s")
            values.append(city_id)
        if role is not None:
            fields.append("role = %s")
            values.append(role)
        if birth_date is not None:
            fields.append("birth_date = %s")
            values.append(birth_date)
        if profile_image is not None:
            fields.append("profile_image = %s")
            values.append(profile_image)
        if status is not None:
            fields.append("status = %s")
            values.append(status)

        if not fields:
            return 0

        fields.append("updated_at = %s")
        values.append(timezone.now())
        values.append(user_id)

        query = f"""
            UPDATE Users
            SET {", ".join(fields)}
            WHERE id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, values)
            return cursor.rowcount

    @staticmethod
    def delete_user(user_id):
        query = "DELETE FROM Users WHERE id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            return cursor.rowcount

    @staticmethod
    def list_users(limit=50, offset=0):
        query = """
            SELECT id, first_name, last_name, email, phone, password, role,
                   city_id, birth_date, profile_image, status,
                   created_at, updated_at
            FROM Users
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [limit, offset])
            return cursor.fetchall()
