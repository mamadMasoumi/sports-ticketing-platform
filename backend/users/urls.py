from django.urls import path
from users.views import RegisterView, PasswordLoginView, RequestOTPView, VerifyOTPView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/password/', PasswordLoginView.as_view(), name='user-login-password'),
    path('login/otp/request/', RequestOTPView.as_view(), name='user-otp-request'),
    path('login/otp/verify/', VerifyOTPView.as_view(), name='user-otp-verify'),
]
