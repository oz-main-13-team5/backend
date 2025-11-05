from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserProfileSerializer, UserProfileUpdateSerializer


User = get_user_model()


class UserProfileView(APIView):
    """
    /me 엔드포인트를 담당하는 View

    GET : 마이페이지 정보 조회
    PATCH : 닉네임/비밀번호 수정
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        로그인한 사용자의 프로필 정보를 반환한다.
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        닉네임과 비밀번호 중 전달된 항목만 수정한다.
        성공 시 updated_fields 목록을 반환한다.
        """
        serializer = UserProfileUpdateSerializer(
            data=request.data,
            context={"request_user": request.user},
        )

        if not serializer.is_valid():
            return Response(
                {"error": "입력값이 올바르지 않습니다", "code": 400, "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated = serializer.validated_data
        updated_fields = []

        nickname = validated.get("nickname")
        if nickname is not None:
            request.user.nickname = nickname
            updated_fields.append("nickname")

        password = validated.get("password")
        if password is not None:
            request.user.set_password(password)
            updated_fields.append("password")

        # 변경 사항이 있다면 저장
        if updated_fields:
            # update_fields에 password를 포함하면 set_password 내부에서 변경된 password 필드까지 저장된다.
            request.user.save(update_fields=updated_fields)
            return Response(
                {
                    "success": True,
                    "message": "회원 정보가 수정되었습니다.",
                    "updated_fields": updated_fields,
                },
                status=status.HTTP_200_OK,
            )

        # 이론상 도달하지 않지만, 안전하게 400 반환
        return Response(
            {"error": "수정할 필드를 최소 1개 이상 입력해주세요.", "code": 400},
            status=status.HTTP_400_BAD_REQUEST,
        )
