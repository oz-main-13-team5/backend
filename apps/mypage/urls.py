from django.urls import path

from .views import (
    UserProfileView,
    UserNicknameUpdateView,
    UserPasswordUpdateView,
)


urlpatterns = [
    path("me", UserProfileView.as_view(), name="my-page"),
    path("me/nickname", UserNicknameUpdateView.as_view(), name="my-page-nickname"),
    path("me/password", UserPasswordUpdateView.as_view(), name="my-page-password"),
]
