from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    마이페이지 조회용 Serializer

    명세서에 따라 username, nickname 등 기본 정보만 반환한다.
    """

    username = serializers.CharField(source="email", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nickname",
            "date_joined",
            "last_login",
            "is_active",
            "is_superuser",
        ]
        read_only_fields = fields


class UserNicknameUpdateSerializer(serializers.Serializer):
    nickname = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=20,
    )


class UserPasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
    )
    new_password = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=8,
        write_only=True,
    )

    def validate(self, attrs):
        user = self.context.get("request_user")
        current = attrs.get("current_password")
        new = attrs.get("new_password")

        if not user.check_password(current):
            raise serializers.ValidationError(
                {"current_password": "현재 비밀번호가 올바르지 않습니다."}
            )
        if current == new:
            raise serializers.ValidationError(
                {"new_password": "현재 비밀번호와 다른 값으로 설정해주세요."}
            )
        return attrs
