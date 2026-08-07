from django.urls import path
from .views import MatchListView, MatchDetailView, ReserveTicketView
from matches.views import CancelReservationView

urlpatterns = [
    path('', MatchListView.as_view()),
    path('<int:match_id>/', MatchDetailView.as_view()),
    path('reserve/', ReserveTicketView.as_view()),
    path('cancel/', CancelReservationView.as_view(), name='reservation-cancel'),
]
