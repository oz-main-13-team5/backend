from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer
from apps.users.services.jwt_service import JWTService


class LoginView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        email = request.data.get("email") or request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {"error": "이메일 또는 비밀번호를 확인해주세요."}, status=400
            )

        token_pair = JWTService.generate_token_pair(user)

        response = Response({"access": token_pair["access"]})
        response.set_cookie(
            key="refresh_token",
            value=token_pair["refresh"],
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 60 * 24 * 14,
        )
        return response
