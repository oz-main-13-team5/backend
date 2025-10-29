from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.services.jwt_service import JWTService


class LogoutView(APIView):
    def post(self, request):
        refresh = request.data.get("refresh")
        if refresh:
            JWTService.blacklist_token(refresh)
        return Response({"detail": "Logged out successfully"}, status=200)
