from django.urls import path
from locations.views import CityListView, VenueListView

urlpatterns = [
    path('cities/', CityListView.as_view(), name='city-list'),
    path('venues/', VenueListView.as_view(), name='venue-list'),
]