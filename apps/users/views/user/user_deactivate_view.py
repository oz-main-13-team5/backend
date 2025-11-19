from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.soft_delete()
        return Response({"회원 탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)
