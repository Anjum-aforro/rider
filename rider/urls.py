from django.urls import path

from .views import RiderListView, RiderDetailView


urlpatterns = [
    # Rider POST
    path(
        "rider/",
        RiderListView.as_view(),
        name="rider-create",
    ),

    # Rider PATCH + DELETE
    path(
        "rider/<int:id>/",
        RiderDetailView.as_view(),
        name="rider-detail",
    ),
]