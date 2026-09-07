from django.urls import path

from .views import RiderListView, RiderDetailView, RiderStatsView, RiderFilterOptionsView ,RiderRateListView, RiderRateDetailView


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
    path("rider/filter-options/", 
         RiderFilterOptionsView.as_view(),
           name="rider-filter-options"),
    path("rates/", RiderRateListView.as_view()),

    path("rates/<int:id>/", RiderRateDetailView.as_view()),
    
]