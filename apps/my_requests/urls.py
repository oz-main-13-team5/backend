from django.urls import path
from .views import MyImageSearchListView

urlpatterns = [
    path("my_requests/", MyImageSearchListView.as_view(), name="my_requests"),
]