from django.urls import path
from .views import MatchListView, MatchDetailView, ReserveTicketView

urlpatterns = [
    path('', MatchListView.as_view()),
    path('<int:match_id>/', MatchDetailView.as_view()),
    path('reserve/', ReserveTicketView.as_view()),
]
