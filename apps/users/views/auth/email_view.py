import random, string
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.users.models.user_auth_email import UserAuthEmail
from apps.users.serializers.email import EmailSendSerializer, EmailVerifySerializer
from apps.users.services.email_service import EmailService


# code email 발송
class EmailSendView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        characters = string.ascii_lowercase + string.digits  # a-z + 0-9
        while True:
            auth_code = "".join(random.choices(characters, k=6))
            if any(c.isalpha() for c in auth_code):  # 최소 한 글자 포함 확인
                break

        expires_at = now() + timedelta(minutes=3)

        UserAuthEmail.objects.update_or_create(
            email=email,
            defaults={
                "auth_code": auth_code,
                "is_verified": False,
                "created_at": now(),
                "expires_at": expires_at,
                "verified_at": None,
            },
        )
        # 메일 발송
        EmailService.send_verification_email(email, auth_code)

        return Response(
            {"detail": "인증번호가 발송 되었습니다."}, status=status.HTTP_200_OK
        )


# code검증
class EmailVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["auth_code"]

        try:
            auth = UserAuthEmail.objects.get(email=email)
        except UserAuthEmail.DoesNotExist:
            return Response(
                {"error": "유효하지 않은 이메일입니다. 다시 시도해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 만료 검사
        if auth.expires_at < now():
            return Response(
                {"error": "코드가 만료되었습니다. 다시 시도해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if auth.auth_code != code:
            return Response(
                {"error": "잘못 된 코드입니다. 다시 시도해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        auth.is_verified = True
        auth.verified_at = now()
        auth.save()

        return Response({"verified": True}, status=status.HTTP_200_OK)
