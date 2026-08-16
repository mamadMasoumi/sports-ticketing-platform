from datetime import timedelta
from django.db import connection, transaction
from django.utils import timezone
from matches.repositories.reservation_repository import ReservationRepository
from payments.repositories.payment_repository import PaymentRepository


class ReservationCancellationService:
    """
    Handles cancellation of a reservation, including refunds for paid tickets.
    """

    REFUND_FULL_AFTER_HOURS = 48
    REFUND_PARTIAL_AFTER_HOURS = 24

    @classmethod
    def _make_naive(cls, dt):
        if dt is None:
            return None
        return dt.replace(tzinfo=None)

    @classmethod
    def _handle_expired_if_needed(cls, reservation_id):
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
                    ReservationRepository.restore_ticket_capacity(cursor, ticket_id)
                    ReservationRepository.update_reservation_status(cursor, res_id, 'Canceled')
        # Commit happens when atomic block exits.

    @classmethod
    def _cancel_reservation_impl(cls, user_id, reservation_id, support_user_id=None, enforce_ownership=True):
        cls._handle_expired_if_needed(reservation_id)

        with transaction.atomic():
            with connection.cursor() as cursor:
                row = ReservationRepository.get_reservation_for_cancel(cursor, reservation_id)
                if not row:
                    raise ValueError("Reservation not found.")

                (res_id, res_user_id, ticket_id, status, expire_time, price, match_date) = row

                if enforce_ownership and res_user_id != user_id:
                    raise ValueError("This reservation does not belong to you.")

                if status in ('Canceled', 'Expired'):
                    raise ValueError("Reservation is already cancelled/expired.")

                now = cls._make_naive(timezone.now())

                if status == 'Reserved':
                    # Unpaid reservation: just cancel, no refund
                    ReservationRepository.restore_ticket_capacity(cursor, ticket_id)
                    ReservationRepository.update_reservation_status(cursor, res_id, 'Canceled')
                    if support_user_id is not None:
                        ReservationRepository.set_support_id(cursor, res_id, support_user_id)
                    return {
                        'reservation_id': res_id,
                        'refund_amount': 0,
                        'new_status': 'Canceled'
                    }

                elif status == 'Paid':
                    time_diff = cls._make_naive(match_date) - now
                    hours_until_match = time_diff.total_seconds() / 3600.0

                    if hours_until_match > cls.REFUND_FULL_AFTER_HOURS:
                        percentage = 1.0
                    elif hours_until_match > cls.REFUND_PARTIAL_AFTER_HOURS:
                        percentage = 0.8
                    else:
                        percentage = 0.5

                    refund_amount = float(price) * percentage

                    # Credit the original ticket owner (not the admin)
                    cursor.execute(
                        "UPDATE Wallet SET balance = balance + %s WHERE user_id = %s",
                        [refund_amount, res_user_id]
                    )

                    # Record refund payment
                    PaymentRepository.create_payment(
                        reservation_id=res_id,
                        user_id=res_user_id,
                        amount=refund_amount,
                        method='Wallet',
                        status='Refunded',
                        transaction_code=None
                    )

                    ReservationRepository.restore_ticket_capacity(cursor, ticket_id)
                    ReservationRepository.update_reservation_status(cursor, res_id, 'Canceled')
                    if support_user_id is not None:
                        ReservationRepository.set_support_id(cursor, res_id, support_user_id)

                    return {
                        'reservation_id': res_id,
                        'refund_amount': refund_amount,
                        'new_status': 'Canceled'
                    }

                else:
                    raise ValueError("Reservation cannot be cancelled in its current state.")

    @classmethod
    def cancel_reservation(cls, user_id, reservation_id):
        """Cancel a reservation as its owner."""
        return cls._cancel_reservation_impl(
            user_id=user_id,
            reservation_id=reservation_id,
            support_user_id=None,
            enforce_ownership=True
        )

    @classmethod
    def admin_cancel_reservation(cls, reservation_id, admin_user_id):
        """Cancel a reservation as support/admin (no ownership check)."""
        return cls._cancel_reservation_impl(
            user_id=None,
            reservation_id=reservation_id,
            support_user_id=admin_user_id,
            enforce_ownership=False
        )