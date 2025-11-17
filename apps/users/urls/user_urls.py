from django.urls import path
from apps.users.views.user.register_view import RegisterView
from apps.users.views.user.user_deactivate_view import UserDeactivateView

urlpatterns = [
    path("signup", RegisterView.as_view(), name="user-register"),
    path("signout", UserDeactivateView.as_view(), name="user-deactivate"),
]
