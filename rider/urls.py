from django.urls import path

from .views import RiderListView, RiderDetailView, RiderStatsView


urlpatterns = [
    path(
        "rider/",
        RiderListView.as_view(),
        name="rider-create",
    ),
    path(
        "rider/<int:id>/",
        RiderDetailView.as_view(),
        name="rider-detail",
    ),
    path(
        "rider/stats/",
        RiderStatsView.as_view(),
        name="rider-stats",
    ),
]