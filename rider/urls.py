from django.urls import path
from .views import RiderListView

urlpatterns = [
    path("rider/", RiderListView.as_view()),
]