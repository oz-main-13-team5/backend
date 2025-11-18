import requests
import uuid
from rest_framework import status

from apps.users.models.user import User
from apps.users.models.user_auth_provider_accounts import UserAuthProviderAccounts
from apps.users.services.jwt_service import JWTService
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView


# 로그인 URL생성
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        google_auth_url = (
            f"{settings.GOOGLE_AUTH_URL}"
            f"?response_type={settings.GOOGLE_AUTH_RESPONSE_TYPE}"
            f"&client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            "&scope=openid%20email%20profile"
        )
        return JsonResponse({"auth_url": google_auth_url})


# OAuth2 인증. 로그인 후 코드를 발급.
class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response(
                {"error": "Missing code"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Access Token 요청
        token_res = requests.post(
            settings.GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )

        if token_res.status_code != 200:
            return Response({"error": "Failed to get token"}, status=400)

        token_json = token_res.json()
        access_token = token_json.get("access_token")

        userinfo_res = requests.get(
            settings.GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        userinfo = userinfo_res.json()

        provider_id = userinfo.get("sub")
        email = userinfo.get("email")
        profile = userinfo.get("picture")

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": email, "is_active": True},
        )

        UserAuthProviderAccounts.objects.get_or_create(
            user=user,
            provider="google",
            provider_user_id=provider_id,
            defaults={"email": email, "profile_image_url": profile},
        )

        jwt_tokens = JWTService.generate_token_pair(user)

        return Response(
            {
                "message": "Google Login Success",
                "access_token": jwt_tokens["access"],
                "refresh_token": jwt_tokens["refresh"],
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
