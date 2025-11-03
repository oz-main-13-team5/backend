from rest_framework import serializers
from apps.users.models.user import User
from apps.users.models.user_auth_email import UserAuthEmail


# 유저 형식 검증 및 생성
class RegisterSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        email = validated_data["email"]
        try:
            auth = UserAuthEmail.objects.get(email=email)
        except UserAuthEmail.DoesNotExist:
            raise serializers.ValidationError("이메일 인증 정보가 존재하지 않습니다.")

        user = User.objects.create_user(
            email=email,
            username=email,
            password=validated_data["password"],
            nickname=validated_data.get("nickname"),
            auth_email_id=auth.id,
        )
        return user
