from datetime import timedelta, timezone as dt_timezone
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.users.services.jwt_service import JWTService
from config import settings


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email") or request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)

        if not user:
            return Response(
                {"error": "이메일 또는 비밀번호를 확인해주세요."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token_pair = JWTService.generate_token_pair(user)
        # === 토큰 만료 정보 계산 ===
        # SimpleJWT 설정에서 ACCESS / REFRESH 수명을 꺼내 사용
        simple_jwt_settings = settings.SIMPLE_JWT

        access_lifetime: timedelta = simple_jwt_settings["ACCESS_TOKEN_LIFETIME"]
        refresh_lifetime: timedelta = simple_jwt_settings["REFRESH_TOKEN_LIFETIME"]

        token_type = simple_jwt_settings.get("AUTH_HEADER_TYPES", ("Bearer",))[0]

        now = timezone.now()
        access_expires_in = int(access_lifetime.total_seconds())
        refresh_expires_at = now + refresh_lifetime

        joined_at = user.date_joined
        if timezone.is_naive(joined_at):
            joined_at = timezone.make_aware(joined_at, timezone.get_default_timezone())
        joined_at_iso = (
            joined_at.astimezone(dt_timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

        last_login = user.last_login
        if last_login:
            if timezone.is_naive(last_login):
                last_login = timezone.make_aware(
                    last_login, timezone.get_default_timezone()
                )
            last_login_iso = (
                last_login.astimezone(dt_timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
        else:
            last_login_iso = None

        refresh_expires_at_iso = (
            refresh_expires_at.astimezone(dt_timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

        # === 최종 response body 구성 ===
        response_data = {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "nickname": user.nickname,
                "is_active": user.is_active,
                "joined_at": joined_at_iso,
                "last_login": last_login_iso,
                # provider 필드는 아직 모델에 없으니 일단 null 로 내려줌
                "provider": None,
            },
            "tokens": {
                "token_type": token_type,
                "access_token": token_pair["access"],
                "access_expires_in": access_expires_in,
                "refresh_expires_at": refresh_expires_at_iso,
            },
        }

        response = Response(response_data, status=status.HTTP_200_OK)

        # refresh 토큰은 쿠키로 세팅 (수명도 SIMPLE_JWT 기준)
        response.set_cookie(
            key="refresh_token",
            value=token_pair["refresh"],
            httponly=True,
            secure=True,
            samesite="None",
            max_age=int(refresh_lifetime.total_seconds()),
        )

        return response

