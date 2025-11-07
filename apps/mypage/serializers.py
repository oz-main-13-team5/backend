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


class UserProfileUpdateSerializer(serializers.Serializer):
    """
    마이페이지 수정용 Serializer

    닉네임과 비밀번호 중 최소 하나는 전달되어야 하며,
    각 필드는 명세서의 기본 정책을 따른다.
    """

    nickname = serializers.CharField(
        required=False,
        allow_blank=False,
        max_length=20,
    )
    password = serializers.CharField(
        required=False,
        allow_blank=False,
        min_length=8,
        write_only=True,
    )

    def validate(self, attrs):
        """닉네임, 비밀번호 둘 다 비어있는 경우를 방지한다."""
        if not attrs:
            raise serializers.ValidationError("수정할 필드를 최소 1개 이상 입력해주세요.")
        return attrs

    def validate_nickname(self, value):
        """닉네임 중복 여부를 확인한다."""
        user = self.context.get("request_user")
        if value and User.objects.exclude(pk=getattr(user, "pk", None)).filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value
