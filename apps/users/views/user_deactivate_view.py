from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def delete(self, request):
        user = request.user
        user.soft_delete()

        return Response(
            {"회원 탈퇴가 완료되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )