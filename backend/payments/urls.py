from django.urls import path
from payments.views import PayForReservationView, PaymentStatusView

urlpatterns = [
    path('pay/', PayForReservationView.as_view(), name='payment-pay'),
    path('status/<int:reservation_id>/', PaymentStatusView.as_view(), name='payment-status'),
]