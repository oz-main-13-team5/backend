from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken as JWTRefreshToken
from apps.users.models.refresh_token import RefreshToken
from apps.users.services.jwt_service import JWTService
import hashlib

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "Refresh token missing"}, status=400)

        hashed_refresh = hashlib.sha256(refresh.encode()).hexdigest()

        try:
            stored_rt = RefreshToken.objects.get(token_hash=hashed_refresh)
        except RefreshToken.DoesNotExist:
            return Response({"detail": "Invalid Refresh Token"}, status=401)

        if stored_rt.is_blacklisted:
            return Response({"detail": "Token is blacklisted"}, status=401)

        try:
            JWTRefreshToken(refresh)  # 유효성 검사
        except Exception:
            stored_rt.blacklist()
            return Response({"detail": "잘못된 접근입니다. 다시 로그인 해주세요."}, status=401)

        new_token_pair = JWTService.generate_token_pair(stored_rt.user)
        stored_rt.blacklist()

        return Response(new_token_pair, status=200)
