from django.urls import path
from .views import UploadHistoryView

urlpatterns = [
    path("", UploadHistoryView.as_view(), name="search-history"),
]
