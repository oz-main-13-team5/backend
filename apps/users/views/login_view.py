from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from apps.users import JWTService

class LoginView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )
        if not user:
            return Response({"error": "이메일 또는 비밀번호를 확인해주세요."}, status=400)

        token = JWTService.generate_access_token(user.id)
        return Response({"token": token})
