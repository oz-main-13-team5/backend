from django.urls import path
from apps.users.views.register_view import RegisterView
from apps.users.views.login_view import LoginView
from apps.users.views.email_verify_view import EmailSendView, EmailVerifyView
from apps.users.views.user_deactivate_view import UserDeactivateView
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.logout_view import LogoutView
from apps.users.views.social_google_view import GoogleLoginView, GoogleCallbackView
from apps.users.views.social_kakao_view import KakaoLoginView, KakaoCallbackView

app_name = "users"

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("signup/send/", EmailSendView.as_view(), name="user-send"),
    path("signup/verify/", EmailVerifyView.as_view(), name="user-verify"),
    path("signout/", UserDeactivateView.as_view(), name="user-deactivate"),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("social/google/login/", GoogleLoginView.as_view()),
    path("social/google/callback/", GoogleCallbackView.as_view()),
    path("social/kakao/login/", KakaoLoginView.as_view(), name="kakao-login"),
    path("social/kakao/callback/", KakaoCallbackView.as_view(), name="kakao-callback"),
]
