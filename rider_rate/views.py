from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import RiderRate
from .serializers import RiderRateSerializer


class RiderRateFilter(filters.FilterSet):

    min_distance = filters.NumberFilter(
        field_name="distance_from",
        lookup_expr="gte"
    )

    max_distance = filters.NumberFilter(
        field_name="distance_to",
        lookup_expr="lte"
    )

    class Meta:
        model = RiderRate
        fields = [
            "rider_type",
            "zone",
            "vehicle",
            "status",
            "rate_type",
            "min_distance",
            "max_distance",
        ]


class RiderRateViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = RiderRateSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_class = RiderRateFilter

    search_fields = [
        "rider_type",
        "zone",
        "vehicle",
        "rate_type",
    ]

    http_method_names = [
        "get",
        "delete",
        "head",
        "options",
    ]

    def get_queryset(self):
        return RiderRate.objects.filter(
            is_deleted=False
        ).order_by("-created_at")

    def destroy(self, request, *args, **kwargs):
        rider_rate = self.get_object()

        rider_rate.is_deleted = True
        rider_rate.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ]
        )

        return Response(
            {
                "message": "Rider rate deleted successfully."
            },
            status=status.HTTP_200_OK
        )