from django.urls import path
from tickets.views import TicketSearchView, TicketDetailView

urlpatterns = [
    path('search/', TicketSearchView.as_view(), name='ticket-search'),
    path('<int:ticket_id>/', TicketDetailView.as_view(), name='ticket-detail'),
]