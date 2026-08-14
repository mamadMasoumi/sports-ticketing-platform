from django.urls import path
from .views import (
    MatchListView,
    MatchDetailView,
    ReserveTicketView,
    CancelReservationView,
    UserBookingsView,
    AdminCancelReservationView,   # <-- new import
)

urlpatterns = [
    path('', MatchListView.as_view()),
    path('<int:match_id>/', MatchDetailView.as_view()),
    path('reserve/', ReserveTicketView.as_view()),
    path('cancel/', CancelReservationView.as_view(), name='reservation-cancel'),
    path('bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('<int:reservation_id>/admin-cancel/', AdminCancelReservationView.as_view(), name='admin-cancel-reservation'),
]