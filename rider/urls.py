from django.urls import path

from .views import RiderListView, RiderDetailView


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
]