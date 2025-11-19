from rest_framework import serializers


# 이메일 형식 검증
class EmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField()


# 이메일 유효성 검증
class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    auth_code = serializers.CharField(min_length=6, max_length=6)
