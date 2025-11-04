from rest_framework import serializers
from apps.users.models.user import User
from apps.users.models.user_auth_email import UserAuthEmail
import re


# 유저 형식 검증 및 생성
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=64)

    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        try:
            auth = UserAuthEmail.objects.get(email=value)
        except UserAuthEmail.DoesNotExist:
            raise serializers.ValidationError("이메일 인증을 먼저 진행해주세요.")

        if not auth.is_verified:
            raise serializers.ValidationError("이메일 인증이 완료되지 않았습니다.")

        return value

    def validate_password(self, value):
        if not re.search(r"[A-Za-z]", value):
            raise serializers.ValidationError("비밀번호에 최소 한 개의 영문자가 포함되어야 합니다.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("비밀번호에 최소 한 개의 숫자가 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("비밀번호에 최소 한 개의 특수문자가 포함되어야 합니다.")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        try:
            auth = UserAuthEmail.objects.get(email=email)
        except UserAuthEmail.DoesNotExist:
            raise serializers.ValidationError("이메일 인증 정보가 존재하지 않습니다.")

        user = User.objects.create_user(
            email=email,
            username=validated_data.get("username", email),
            password=validated_data["password"],
            nickname=validated_data.get("nickname"),
            auth_email_id=auth.id,
        )
        return user
