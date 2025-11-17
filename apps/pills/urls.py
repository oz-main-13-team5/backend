from django.urls import path
from apps.pills.views.pill_list_view import PillListView
from apps.pills.views.pill_detail_view import PillDetailView
from apps.pills.views.pill_search_view import PillSearchView

urlpatterns = [
    path('search/', PillSearchView.as_view(), name='pill-search'),
    path('', PillListView.as_view(), name='pill-list'),
    path("<str:item_seq>/", PillDetailView.as_view(), name="pill-detail"),
]
