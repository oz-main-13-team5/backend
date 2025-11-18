from django.urls import path

from .views import (
    UserProfileView,
    UserNicknameUpdateView,
    UserPasswordUpdateView,
)


urlpatterns = [
    path("", UserProfileView.as_view(), name="my-page"),
    path("nickname/", UserNicknameUpdateView.as_view(), name="my-page-nickname"),
    path("password/", UserPasswordUpdateView.as_view(), name="my-page-password"),
]
