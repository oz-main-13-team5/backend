from rest_framework.routers import DefaultRouter
from .views import BookmarkViewSet

router = DefaultRouter()
router.register(r"", BookmarkViewSet, basename="bookmark")

urlpatterns = router.urls
