from django.urls import path
from reports.views import (
    SubmitReportView,
    UserReportsView,
    AllReportsView,
    ReviewReportView,
)

urlpatterns = [
    path('submit/', SubmitReportView.as_view(), name='report-submit'),
    path('mine/', UserReportsView.as_view(), name='report-mine'),
    path('all/', AllReportsView.as_view(), name='report-all'),
    path('<int:report_id>/review/', ReviewReportView.as_view(), name='report-review'),
]