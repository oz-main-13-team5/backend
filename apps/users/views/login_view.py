from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from apps.users.services.jwt_service import JWTService


class LoginView(APIView):

    def post(self, request):
        email = request.data.get("email") or request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            return Response(
                {"error": "이메일 또는 비밀번호를 확인해주세요."}, status=400
            )

        token_pair = JWTService.generate_token_pair(user)

        response = Response(
            {"message": "Login Success", "access": token_pair["access"]},
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="refresh_token",
            value=token_pair["refresh"],
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 60 * 24 * 14,
        )
        return response
