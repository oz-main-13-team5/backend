from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.users.models.user import User
from apps.users.models.user_auth_email import UserAuthEmail

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "nickname", "password"]

    def validate_email(self, value):
        try:
            auth = UserAuthEmail.objects.get(email=value)
        except UserAuthEmail.DoesNotExist:
            raise serializers.ValidationError("이메일 인증을 먼저 진행해주세요.")
        if not auth.is_verified:
            raise serializers.ValidationError("이메일 인증이 완료되지 않았습니다.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value