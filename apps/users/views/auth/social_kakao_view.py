import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
from apps.users.models.user import User
from apps.users.models.user_auth_provider_accounts import UserAuthProviderAccounts
from apps.users.services.jwt_service import JWTService


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        kakao_auth_url = (
            f"{settings.KAKAO_AUTH_URL}"
            f"?client_id={settings.KAKAO_CLIENT_ID}"
            f"&redirect_uri={settings.KAKAO_REDIRECT_URI}"
            "&response_type=code"
            "&scope=profile_nickname,profile_image"
        )
        return Response({"auth_url": kakao_auth_url})


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return Response({"error": "Missing code"}, status=400)

        # 토큰 요청
        token_res = requests.post(
            settings.KAKAO_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_CLIENT_ID,
                "client_secret": settings.KAKAO_CLIENT_SECRET,
                "redirect_uri": settings.KAKAO_REDIRECT_URI,
                "code": code,
            },
            headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
        )

        if token_res.status_code != 200:
            return Response({"error": "Failed to get token"}, status=400)

        access_token = token_res.json().get("access_token")
        if not access_token:
            return Response({"error": "No access_token"}, status=400)

        # 카카오 유저 정보 조회
        userinfo_res = requests.get(
            settings.KAKAO_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        userinfo = userinfo_res.json()

        # 카카오 유저 정보 조회 결과 처리
        kakao_id = userinfo.get("id")
        if not kakao_id:
            return Response(
                {"error": "Kakao ID not found", "details": userinfo}, status=400
            )

        kakao_account = userinfo.get("kakao_account", {})
        profile = kakao_account.get("profile", {})
        nickname = profile.get("profile_nickname")
        profile_image = profile.get("profile_image_url")

        # 이메일 없이 로그인 가능하도록 처리로직
        email = f"{nickname}@example.com"
        # username을 nickname + '@' + email 로 설정
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "is_active": True,
            },
        )

        UserAuthProviderAccounts.objects.update_or_create(
            user=user,
            provider="kakao",
            provider_user_id=kakao_id,
            defaults={"email": email, "profile_image_url": profile_image},
        )

        tokens = JWTService.generate_token_pair(user)
        return Response(
            {
                "message": "Kakao Login Success",
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
