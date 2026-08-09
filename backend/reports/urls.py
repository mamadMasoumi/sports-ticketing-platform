from django.urls import path
from reports.views import SubmitReportView, UserReportsView

urlpatterns = [
    path('submit/', SubmitReportView.as_view(), name='report-submit'),
    path('mine/', UserReportsView.as_view(), name='report-mine'),
]