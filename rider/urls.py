from django.urls import path
from .views import RiderListView, RiderDetailView, RiderDepositView


urlpatterns = [
    path("rider/", RiderListView.as_view()),
    path("rider/<int:id>/", RiderDetailView.as_view()),
    path(
        "rider/<int:id>/deposit/",
        RiderDepositView.as_view(),
    ),
]
