from django.urls import path
from apps.users.views.register_view import RegisterView
from apps.users.views.login_view import LoginView
from apps.users.views.email_verify_view import EmailSendView, EmailVerifyView
from apps.users.views.user_deactivate_view import UserDeactivateView

app_name = "users"

urlpatterns = [
    path('REQ_USER_001/', RegisterView.as_view(), name="user-register"),
    path('REQ_USER_002/', LoginView.as_view(), name="user-login"),
    path('REQ_USER_003/send/', EmailSendView.as_view(), name="user-send"),
    path('REQ_USER_003/verify/', EmailVerifyView.as_view(), name="user-verify"),
    path('REQ_USER_004/', UserDeactivateView.as_view(), name="user-deactivate"),
]