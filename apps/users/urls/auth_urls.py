from django.urls import path
from apps.users.views.auth.email_view import EmailSendView
from apps.users.views.auth.email_view import EmailVerifyView
from apps.users.views.auth.login_view import LoginView
from apps.users.views.auth.logout_view import LogoutView
from apps.users.views.auth.token_refresh_view import TokenRefreshView
from apps.users.views.auth.social_google_view import GoogleLoginView, GoogleCallbackView
from apps.users.views.auth.social_kakao_view import KakaoLoginView, KakaoCallbackView

urlpatterns = [
    path("email-send", EmailSendView.as_view(), name="auth-email-send"),
    path("email-verify", EmailVerifyView.as_view(), name="auth-email-verify"),
    path("login", LoginView.as_view(), name="auth-login"),
    path("logout", LogoutView.as_view(), name="auth-logout"),
    path("token/refresh", TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("social/google/login", GoogleLoginView.as_view(), name="auth-google-login"),
    path(
        "social/google/callback",
        GoogleCallbackView.as_view(),
        name="auth-google-callback",
    ),
    path("social/kakao/login", KakaoLoginView.as_view(), name="auth-kakao-login"),
    path(
        "social/kakao/callback", KakaoCallbackView.as_view(), name="auth-kakao-callback"
    ),
]
