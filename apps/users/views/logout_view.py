from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"detail": "refresh_token is required"}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트 등록 ✅
        except Exception:
            return Response({"detail": "Invalid token"}, status=400)

        return Response({"message": "Logout successful"}, status=200)
