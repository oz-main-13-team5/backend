import requests
import uuid
from rest_framework import status

from apps.users.models.user import User
from apps.users.models.user_auth_provider_accounts import UserAuthProviderAccounts
from apps.users.services.jwt_service import JWTService

from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView


class GoogleLoginView(APIView):
    def get(self, request):
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            "&scope=openid%20email%20profile"
        )
        return JsonResponse({"auth_url": google_auth_url})


class GoogleCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "Missing code"}, status=400)

        # 1. Access Token 요청
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_res = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)
        token_json = token_res.json()
        access_token = token_json.get("access_token")

        if not access_token:
            return JsonResponse({"error": "Failed to get access token"}, status=400)

        # 2. UserInfo 요청
        userinfo_res = requests.get(
            settings.GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        userinfo = userinfo_res.json()

        provider_account_id = userinfo.get("sub")
        email = userinfo.get("email")
        profile = userinfo.get("picture")

        # 기존 Provider 계정 조회
        try:
            provider_account = UserAuthProviderAccounts.objects.get(
                provider="google", provider_user_id=provider_account_id
            )
            user = provider_account.user
        except UserAuthProviderAccounts.DoesNotExist:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "id": uuid.uuid4(),
                    "username": email,
                    "is_active": True,
                },
            )

            # Provider 계정 생성
            UserAuthProviderAccounts.objects.get_or_create(
                user=user,
                provider="google",
                provider_user_id=provider_account_id,
                defaults={
                    "email": email,
                    "profile_image_url": profile,
                },
            )

        # ✅ 4. JWT 발급
        jwt_token = JWTService.generate_token_pair(user)

        return JsonResponse(
            {
                "message": "Google Login Success",
                "access_token": jwt_token["access"],
                "refresh_token": jwt_token["refresh"],
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
