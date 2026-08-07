import uuid
from django.db import connection, transaction
from django.utils import timezone
from payments.repositories.payment_repository import PaymentRepository
from matches.repositories.reservation_repository import ReservationRepository


class PaymentService:

    @staticmethod
    def _make_naive(dt):
        """Convert a datetime to naive for safe DB comparison."""
        if dt is None:
            return None
        return dt.replace(tzinfo=None)

    @staticmethod
    def _get_reservation_with_price(cursor, reservation_id):
        query = """
            SELECT r.id, r.user_id, r.ticket_id, r.status,
                   r.reserve_time, r.expire_time, t.price
            FROM Reservations r
            JOIN Tickets t ON r.ticket_id = t.id
            WHERE r.id = %s
            FOR UPDATE
        """
        cursor.execute(query, [reservation_id])
        return cursor.fetchone()

    @classmethod
    def pay_for_reservation(cls, user_id, reservation_id, method):
        # First, handle any expired reservation in a separate atomic block
        # so that capacity restore + cancel commit even if we later raise.
        cls._handle_expired_if_needed(reservation_id)

        with transaction.atomic():
            with connection.cursor() as cursor:
                row = cls._get_reservation_with_price(cursor, reservation_id)
                if not row:
                    raise ValueError("Reservation not found.")

                (res_id, res_user_id, ticket_id, status,
                 reserve_time, expire_time, price) = row

                if res_user_id != user_id:
                    raise ValueError("This reservation does not belong to you.")

                if status == 'Paid':
                    raise ValueError("This reservation is already paid.")
                if status == 'Canceled':
                    raise ValueError("This reservation is cancelled.")
                if status != 'Reserved':
                    raise ValueError("Reservation is not in a payable state.")

                # At this point we know the reservation is still fresh (expiry handled)
                # Simulate payment success
                payment_status = 'Success'
                transaction_code = f"TXN{uuid.uuid4().hex[:12].upper()}"

                payment_id = PaymentRepository.create_payment(
                    reservation_id=res_id,
                    user_id=user_id,
                    amount=price,
                    method=method,
                    status=payment_status,
                    transaction_code=transaction_code
                )

                cursor.execute(
                    "UPDATE Reservations SET status = 'Paid' WHERE id = %s",
                    [res_id]
                )

            return {
                'payment_id': payment_id,
                'reservation_id': res_id,
                'amount': str(price),
                'status': payment_status,
                'transaction_code': transaction_code
            }

    @classmethod
    def _handle_expired_if_needed(cls, reservation_id):
        """Check and auto-cancel an expired reservation in its own transaction."""
        now = cls._make_naive(timezone.now())

        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, status, expire_time, ticket_id "
                    "FROM Reservations WHERE id = %s FOR UPDATE",
                    [reservation_id]
                )
                row = cursor.fetchone()
                if not row:
                    return

                res_id, status, expire_time, ticket_id = row
                expire_time = cls._make_naive(expire_time)

                if status in ('Canceled', 'Expired'):
                    return

                if expire_time and expire_time < now:
                    ReservationRepository.restore_ticket_capacity(
                        cursor, ticket_id
                    )
                    ReservationRepository.update_reservation_status(
                        cursor, res_id, 'Canceled'
                    )
                    # commit on exit; then raise outside
                    return

        # If we got here, no expiry => continue