from django.urls import path, include
from apps.pills.views.pill_list_view import PillListView
from apps.pills.views.pill_detail_view import PillDetailView
from apps.pills.views.pill_search_view import PillSearchView

urlpatterns = [
    path("image/", include("apps.pills.search_uploads.urls")),
    path("search-histories/", include("apps.pills.search_histories.urls")),
    path('search/', PillSearchView.as_view(), name='pill-search'),
    path('', PillListView.as_view(), name='pill-list'),
    path("<str:item_seq>/", PillDetailView.as_view(), name="pill-detail"),
]