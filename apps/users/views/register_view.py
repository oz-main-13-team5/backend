from rest_framework.generics import CreateAPIView
from apps.users.serializers.user import RegisterSerializer

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
