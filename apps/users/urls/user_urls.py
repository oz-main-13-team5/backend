from django.urls import path
from apps.users.views.user.register_view import RegisterView
from apps.users.views.user.user_deactivate_view import UserDeactivateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("deactivate/", UserDeactivateView.as_view(), name="user-deactivate"),
]
