from django.urls import path

from apps.uploads.views import PillImageUploadView

app_name = "uploads"

urlpatterns = [
    path("pills/image/", PillImageUploadView.as_view(), name="pill-image-upload"),
]
