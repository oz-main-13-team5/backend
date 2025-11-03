from rest_framework.generics import CreateAPIView
from rest_framework.renderers import JSONRenderer
from apps.users.serializers.user import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = [JSONRenderer]
