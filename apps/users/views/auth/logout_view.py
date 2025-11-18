from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.users.services.jwt_service import JWTService


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        JWTService.blacklist_token(refresh_token)

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token", samesite="Lax")
        return response
