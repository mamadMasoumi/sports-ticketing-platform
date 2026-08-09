from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/matches/', include('matches.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/tickets/', include('tickets.urls')),
    path('api/reports/', include('reports.urls')),
]