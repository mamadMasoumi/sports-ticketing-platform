from datetime import timedelta
from django.db import connection, transaction
from django.utils import timezone
from matches.repositories.reservation_repository import ReservationRepository
from payments.repositories.payment_repository import PaymentRepository


class ReservationCancellationService:
    """
    Handles cancellation of a reservation, including refunds for paid tickets.
    """

    # Refund percentage tiers based on time until match
    REFUND_FULL_AFTER_HOURS = 48      # more than 48h → 100%
    REFUND_PARTIAL_AFTER_HOURS = 24   # 24–48h → 80%
    # less than 24h → 50%

    @classmethod
    def _make_naive(cls, dt):
        """Convert a datetime to naive (no tzinfo) for safe DB comparison."""
        if dt is None:
            return None
        return dt.replace(tzinfo=None)

    @classmethod
    def cancel_reservation(cls, user_id, reservation_id):
        # First, handle any expired reservation in a separate atomic block
        # so that capacity restoration and status change are committed
        # *before* we raise any user‑facing error.
        cls._handle_expired_if_needed(reservation_id)

        with transaction.atomic():
            with connection.cursor() as cursor:
                row = ReservationRepository.get_reservation_for_cancel(
                    cursor, reservation_id
                )

                if not row:
                    raise ValueError("Reservation not found.")

                (res_id, res_user_id, ticket_id, status,
                 expire_time, price, match_date) = row

                # Ownership check
                if res_user_id != user_id:
                    raise ValueError(
                        "This reservation does not belong to you."
                    )

                # State checks (expired already handled above)
                if status in ('Canceled', 'Expired'):
                    raise ValueError(
                        "Reservation is already cancelled/expired."
                    )

                # Proceed with normal cancellation logic
                now = cls._make_naive(timezone.now())

                if status == 'Reserved':
                    # Unpaid reservation: just cancel, no refund
                    ReservationRepository.restore_ticket_capacity(
                        cursor, ticket_id
                    )
                    ReservationRepository.update_reservation_status(
                        cursor, res_id, 'Canceled'
                    )
                    return {
                        'reservation_id': res_id,
                        'refund_amount': 0,
                        'new_status': 'Canceled'
                    }

                elif status == 'Paid':
                    # Paid reservation: calculate refund
                    time_diff = cls._make_naive(match_date) - now
                    hours_until_match = time_diff.total_seconds() / 3600.0

                    if hours_until_match > cls.REFUND_FULL_AFTER_HOURS:
                        percentage = 1.0
                    elif hours_until_match > cls.REFUND_PARTIAL_AFTER_HOURS:
                        percentage = 0.8
                    else:
                        percentage = 0.5

                    refund_amount = float(price) * percentage

                    # Update wallet
                    cursor.execute(
                        "UPDATE Wallet SET balance = balance + %s "
                        "WHERE user_id = %s",
                        [refund_amount, user_id]
                    )

                    # Record refund payment
                    PaymentRepository.create_payment(
                        reservation_id=res_id,
                        user_id=user_id,
                        amount=refund_amount,
                        method='Wallet',
                        status='Refunded',
                        transaction_code=None
                    )

                    # Restore capacity
                    ReservationRepository.restore_ticket_capacity(
                        cursor, ticket_id
                    )

                    # Cancel reservation
                    ReservationRepository.update_reservation_status(
                        cursor, res_id, 'Canceled'
                    )

                    return {
                        'reservation_id': res_id,
                        'refund_amount': refund_amount,
                        'new_status': 'Canceled'
                    }

                else:
                    raise ValueError(
                        "Reservation cannot be cancelled in its current state."
                    )

    @classmethod
    def _handle_expired_if_needed(cls, reservation_id):
        """
        Checks whether the reservation is expired. If so, restores ticket
        capacity and sets status to 'Canceled' in its own short transaction
        that is guaranteed to commit, then raises an error.
        """
        now = cls._make_naive(timezone.now())

        with transaction.atomic():
            with connection.cursor() as cursor:
                # Lock the reservation to read expiry
                cursor.execute(
                    "SELECT id, status, expire_time, ticket_id "
                    "FROM Reservations WHERE id = %s FOR UPDATE",
                    [reservation_id]
                )
                row = cursor.fetchone()
                if not row:
                    return  # will be caught later

                res_id, status, expire_time, ticket_id = row
                expire_time = cls._make_naive(expire_time)

                if status in ('Canceled', 'Expired'):
                    return  # already dead, let the main method reject it

                if expire_time and expire_time < now:
                    # Expired – restore capacity and mark cancelled
                    ReservationRepository.restore_ticket_capacity(
                        cursor, ticket_id
                    )
                    ReservationRepository.update_reservation_status(
                        cursor, res_id, 'Canceled'
                    )
                    # Commit happens automatically when this atomic block exits
                    # without an exception. Then we raise outside.
                    return

        # If we get here, the reservation was not expired – proceed normally.