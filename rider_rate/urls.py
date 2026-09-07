from rest_framework.routers import DefaultRouter

from .views import RiderRateViewSet


router = DefaultRouter()

router.register(
    "rider-rates",
    RiderRateViewSet,
    basename="rider-rate"
)

urlpatterns = router.urls