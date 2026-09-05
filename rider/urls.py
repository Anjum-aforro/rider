from django.urls import path
from .views import RiderListView,RiderDetailView

urlpatterns = [
    path("rider/", RiderListView.as_view()),
    path("rider/<int:pk>/", RiderDetailView.as_view()),
    
]