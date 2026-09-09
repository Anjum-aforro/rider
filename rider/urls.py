from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RiderActivityLogView,
    RiderCODView,
    RiderEarningsPayoutView,
    RiderIncentiveHistoryView,
    RiderListView,
    RiderDetailView,
    RiderQuickStatsView,
    RiderStatsView,
    RiderFilterOptionsView,
    RiderRateListView,
    RiderRateDetailView,
    RiderRateViewSet,
    RiderMonitoringView,
    RiderRateFilterView,
    RiderOrderListView
)


router = DefaultRouter()

router.register(
    "rider-rates",
    RiderRateViewSet,
    basename="rider-rate",
)


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

    path(
        "rider/filter-options/",
        RiderFilterOptionsView.as_view(),
        name="rider-filter-options",
    ),

    path(
        "rates/",
        RiderRateListView.as_view(),
    ),

    path(
        "rates/<int:id>/",
        RiderRateDetailView.as_view(),
    ),

    path(
        "api/",
        include(router.urls),
    ),
    path(
    "riders/<int:rider_id>/monitoring/",
    RiderMonitoringView.as_view()
    ),

    path("rider-rate-filters/", 
         RiderRateFilterView.as_view(), 
         name="rider-rate-filters"),

    path(
    "rider/<int:rider_id>/quick-stats/",
    RiderQuickStatsView.as_view(),
    name="rider-quick-stats"
),

   path(
    "rider/<int:rider_id>/orders/",
    RiderOrderListView.as_view(),
    name="rider-orders"
),


   path(
    "rider/<int:rider_id>/earnings-payouts/",
    RiderEarningsPayoutView.as_view(),
    name="rider-earnings-payouts"
),

   path(
    "rider/<int:rider_id>/cod/",
    RiderCODView.as_view(),
    name="rider-cod"
),

   path(
    "rider/<int:rider_id>/incentive-history/",
    RiderIncentiveHistoryView.as_view(),
    name="rider-incentive-history"
),

   path(
    "rider/<int:rider_id>/activity-log/",
    RiderActivityLogView.as_view(),
    name="rider-activity-log"
),


]