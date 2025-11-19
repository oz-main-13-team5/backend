from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    UserProfileSerializer,
    UserNicknameUpdateSerializer,
    UserPasswordUpdateSerializer,
)


User = get_user_model()


class UserProfileView(APIView):
    """
    /mypage/ 엔드포인트를 담당하는 View (조회 전용)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserNicknameUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserNicknameUpdateSerializer(
            data=request.data, context={"request_user": request.user}
        )
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.nickname = serializer.validated_data["nickname"]
        request.user.save(update_fields=["nickname"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPasswordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserPasswordUpdateSerializer(
            data=request.data, context={"request_user": request.user}
        )
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMeView(APIView):
    """
    /users/me (GET, PATCH) 명세 대응용 View.
    GET은 UserProfileView와 동일, PATCH는 닉네임 수정과 동일 동작을 수행한다.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserNicknameUpdateSerializer(
            data=request.data, context={"request_user": request.user}
        )
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.nickname = serializer.validated_data["nickname"]
        request.user.save(update_fields=["nickname"])
        return Response(status=status.HTTP_204_NO_CONTENT)
