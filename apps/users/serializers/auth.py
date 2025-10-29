from rest_framework import serializers
from apps.users.models.user_auth_email import UserAuthEmail


# 이메일 형식 검증
class EmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField()


# 이메일 유효성 검증
class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    auth_code = serializers.CharField(max_length=6)
