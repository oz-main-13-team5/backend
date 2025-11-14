from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.users.models.user import User
from apps.users.models.user_auth_email import UserAuthEmail
from apps.users.serializers.register import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        email = validated_data["email"]

        # 이메일 인증 여부 확인
        auth = UserAuthEmail.objects.get(email=email)

        # User 생성
        user = User.objects.create_user(
            email=email,
            username=email,
            nickname=validated_data.get("nickname"),
            password=validated_data["password"],
            auth_email_id=auth.id,
        )
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {"detail": "회원가입이 완료되었습니다.", "user_id": str(user.id)},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
