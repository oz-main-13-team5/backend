from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.serializers.register import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"detail": "회원가입이 완료되었습니다.", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
