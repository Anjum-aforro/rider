from django.db.models import Q

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, status, viewsets

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.filters import SearchFilter

from drf_spectacular.utils import extend_schema, OpenApiParameter


from .models import Rider, RiderPayout, RiderRate
from .serializers import (
    RiderEarningsPayoutSerializer,
    RiderSerializer,
    RiderListSerializer,
    LegacyRiderRateSerializer,
    RiderRateGetSerializer,
    RiderOrderSerializer,
    RiderRateSerializer,
    
)


class RiderListView(APIView):

    parser_classes =[MultiPartParser, FormParser, JSONParser]

    @extend_schema(
        parameters=[
            OpenApiParameter("search", str, OpenApiParameter.QUERY),
            OpenApiParameter("rider_type", str, OpenApiParameter.QUERY),
            OpenApiParameter("assigned_store", str, OpenApiParameter.QUERY),
            OpenApiParameter("assigned_zone", str, OpenApiParameter.QUERY),
            OpenApiParameter("payout_method", str, OpenApiParameter.QUERY),
            OpenApiParameter("online_status", str, OpenApiParameter.QUERY),
            OpenApiParameter("account_status", str, OpenApiParameter.QUERY),
            OpenApiParameter("cash_filter", str, OpenApiParameter.QUERY),
            OpenApiParameter("page", int, OpenApiParameter.QUERY),
            OpenApiParameter("page_size", int, OpenApiParameter.QUERY),
        ],
        responses={200: RiderListSerializer(many=True)},
    )
    def get(self, request):
        riders = Rider.objects.filter(is_deleted=False).order_by("-created_at")

        search = request.GET.get("search")

        if search:
            riders = riders.filter(
                Q(name__icontains=search)
                | Q(phone__icontains=search)
                | Q(vehicle_number__icontains=search)
                | Q(assigned_store__icontains=search)
            )

        rider_type = request.GET.get("rider_type")
        if rider_type:
            riders = riders.filter(rider_type=rider_type)

        assigned_store = request.GET.get("assigned_store")
        if assigned_store:
            riders = riders.filter(assigned_store=assigned_store)

        assigned_zone = request.GET.get("assigned_zone")
        if assigned_zone:
            riders = riders.filter(assigned_zone=assigned_zone)

        payout_method = request.GET.get("payout_method")
        if payout_method:
            riders = riders.filter(payout_method=payout_method)

        account_status = request.GET.get("account_status")
        if account_status:
            riders = riders.filter(account_status=account_status)

        online_status = request.GET.get("online_status")
        if online_status:
            riders = riders.filter(online_status=online_status)

        cash_filter = request.GET.get("cash_filter")

        if cash_filter == "above_0":
            riders = riders.filter(has_undeposited_cash=True)
        elif cash_filter == "zero":
            riders = riders.filter(has_undeposited_cash=False)

        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))

        total_count = riders.count()

        start = (page - 1) * page_size
        end = start + page_size

        riders = riders[start:end]

        serializer = RiderListSerializer(riders, many=True)

        return Response(
            {
                "status": True,
                "data": serializer.data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                },
                "message": "Riders retrieved successfully",
            }
        )

    @extend_schema(
        request=RiderSerializer,
        responses={201: RiderSerializer},
    )
    def post(self, request):
        serializer = RiderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": False,
                    "errors": serializer.errors,
                    "message": "Rider creation failed",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        rider = serializer.save()

        return Response(
            {
                "status": True,
                "data": RiderSerializer(rider).data,
                "message": "Rider created successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class RiderStatsView(APIView):

    @extend_schema(
        responses={200: dict},
    )
    def get(self, request):
        riders = Rider.objects.filter(is_deleted=False)

        total_fleet = riders.count()

        active_online = riders.filter(online_status=True).count()

        on_delivery = riders.filter(current_order__isnull=False).count()

        total_cash_in_hand = sum(
            rider.cash_in_hand for rider in riders
        )

        return Response(
            {
                "status": True,
                "data": {
                    "total_fleet": f"{total_fleet}",
                    "active_online": f"{active_online}",
                    "on_delivery": f"{on_delivery}",
                    "total_cash_in_hand": f"₹{total_cash_in_hand:,.0f}",
                },
                "message": "Rider stats retrieved successfully",
            }
        )

class RiderQuickStatsView(APIView):

    @extend_schema(
        responses={200: dict},
    )
    def get(self, request, rider_id):
        try:
            rider = Rider.objects.get(
                id=rider_id,
                is_deleted=False
            )
        except Rider.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Rider not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "status": True,
                "data": {
                    "total_orders_delivered": f"{rider.total_orders_delivered:,}",
                    "average_rating": f"{rider.average_rating:.1f}",
                    "completion_rate": f"{rider.completion_rate:.1f}%",
                    "total_earnings": f"₹{rider.total_earnings:,.0f}",
                },
                "message": "Rider quick stats retrieved successfully"
            },
            status=status.HTTP_200_OK
        )
class RiderDetailView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        responses={200: RiderSerializer},
    )
    def get(self, request, id):
        try:
            rider = Rider.objects.get(
                id=id,
                is_deleted=False,
            )
        except Rider.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Rider not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RiderSerializer(rider)

        return Response(
            {
                "status": True,
                "data": {
                    "profile_information": {
                        "id": serializer.data["id"],
                        "name": serializer.data["name"],
                        "phone": serializer.data["phone"],
                        "address": serializer.data["address"],
                        "rider_type": serializer.data["rider_type"],
                        "assigned_store": serializer.data["assigned_store"],
                        "assigned_zone": serializer.data["assigned_zone"],
                        "vehicle_number": serializer.data["vehicle_number"],
                    },
                    "payment_information": {
                        "base_salary": serializer.data["base_salary"],
                        "per_order_rate": serializer.data["per_order_rate"],
                        "per_km_rate": serializer.data["per_km_rate"],
                        "payout_method": serializer.data["payout_method"],
                        "upi_id": serializer.data["upi_id"],
                        "bank_account_number": serializer.data["bank_account_number"],
                        "ifsc_code": serializer.data["ifsc_code"],
                        "account_holder_name": serializer.data["account_holder_name"],
                    },
                    "documents": {
                        "driving_license_number": serializer.data["driving_license_number"],
                        "driving_license_document": serializer.data["driving_license_document"],
                        "driving_license_verification_status": serializer.data["driving_license_verification_status"],
                        "aadhaar_number": serializer.data["aadhaar_number"],
                        "aadhaar_document": serializer.data["aadhaar_document"],
                        "aadhaar_verification_status": serializer.data["aadhaar_verification_status"],
                        "vehicle_rc_number": serializer.data["vehicle_rc_number"],
                        "vehicle_rc_document": serializer.data["vehicle_rc_document"],
                        "vehicle_rc_verification_status": serializer.data["vehicle_rc_verification_status"],
                    },
                    "rider_status": {
                        "account_status": serializer.data["account_status"],
                        "is_deleted": serializer.data["is_deleted"],
                        "activate_immediately": serializer.data["activate_immediately"],
                        "online_status": serializer.data["online_status"],
                        "current_order": serializer.data["current_order"],
                        "cash_in_hand": serializer.data["cash_in_hand"],
                        "has_undeposited_cash": serializer.data["has_undeposited_cash"],
                    },
                    "timestamps": {
                        "created_at": serializer.data["created_at"],
                        "updated_at": serializer.data["updated_at"],
                    },
                },
                "message": "Rider retrieved successfully",
            }
        )

    @extend_schema(
        request=RiderSerializer,
        responses={200: RiderSerializer},
    )
    def patch(self, request, id):
        try:
            rider = Rider.objects.get(
                id=id,
                is_deleted=False,
            )
        except Rider.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Rider not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RiderSerializer(
            rider,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "status": False,
                    "errors": serializer.errors,
                    "message": "Rider update failed",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        rider = serializer.save()

        return Response(
            {
                "status": True,
                "data": RiderSerializer(rider).data,
                "message": "Rider updated successfully",
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={200: dict},
    )
    def delete(self, request, id):
        try:
            rider = Rider.objects.get(
                id=id,
                is_deleted=False,
            )
        except Rider.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Rider not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        rider.is_deleted = True
        rider.account_status = Rider.AccountStatus.INACTIVE

        rider.save(
            update_fields=[
                "is_deleted",
                "account_status",
                "updated_at",
            ]
        )

        return Response(
            {
                "status": True,
                "message": "Rider deleted successfully",
            },
            status=status.HTTP_200_OK,
        )


class RiderFilterOptionsView(APIView):

    @extend_schema(
        responses={200: dict},
    )
    def get(self, request):
        return Response(
            {
                "status": True,
                "data": {
                    "rider_type": [
                        "Salary-based",
                        "Per-order",
                    ],
                    "assigned_store": [
                        "BTM Layout Stage 2",
                        "Bellandur Outer Ring",
                        "HSR Layout Sector 2",
                        "Indiranagar Darkstore",
                        "Jayanagar 4th Block",
                        "Koramangala Hub",
                        "Malleswaram Central",
                        "Whitefield Depot",
                    ],
                    "account_status": [
                        "Active",
                        "Inactive",
                        "Block",
                        "Pending",
                        "Suspend",
                        "Rejected",
                    ],
                },
            }
        )


class RiderRateListView(APIView):

    @extend_schema(
        request=LegacyRiderRateSerializer,
        responses={201: LegacyRiderRateSerializer},
    )
    def post(self, request):
        serializer = LegacyRiderRateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": False,
                    "errors": serializer.errors,
                    "message": "Rider rate creation failed",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        rider_rate = serializer.save()

        return Response(
            {
                "status": True,
                "data": LegacyRiderRateSerializer(rider_rate).data,
                "message": "Rider rate created successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class RiderRateDetailView(APIView):

    @extend_schema(
        request=LegacyRiderRateSerializer,
        responses={200: LegacyRiderRateSerializer},
    )
    def patch(self, request, id):
        try:
            rider_rate = RiderRate.objects.get(id=id)
        except RiderRate.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Rider rate not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LegacyRiderRateSerializer(
            rider_rate,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "status": False,
                    "errors": serializer.errors,
                    "message": "Rider rate update failed",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        rider_rate = serializer.save()

        return Response(
            {
                "status": True,
                "data": LegacyRiderRateSerializer(rider_rate).data,
                "message": "Rider rate updated successfully",
            },
            status=status.HTTP_200_OK,
        )


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
        ]


class RiderRateViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = RiderRateGetSerializer

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

class RiderMonitoringView(APIView):

    @extend_schema(
        responses={200: dict},
    )
    def get(self, request, rider_id):
        try:
            rider = Rider.objects.get(
                id=rider_id,
                is_deleted=False
            )
        except Rider.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Rider not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        assignment = getattr(rider, "current_assignment", None)

        login_logs = rider.login_logout_logs.all().order_by("-time")

        attendance = rider.attendance.order_by("-id").first()

        return Response(
            {
                "status": True,
                "data": {
                    "current_assignment": {
                        "order_id": assignment.order_id if assignment else None,
                        "status": assignment.status if assignment else None,
                        "pickup": assignment.pickup if assignment else None,
                        "drop": assignment.drop if assignment else None,
                        "customer": assignment.customer if assignment else None,
                        "order_value": (
                            f"₹{assignment.order_value:,.2f}"
                            if assignment and assignment.order_value is not None
                            else None
                        ),
                    },
                    "rider_status": {
                        "status": rider.online_status
                    },
                    "last_location": {
                        "zone": rider.assigned_zone
                    },
                    "login_logout_log": [
                        {
                            "time": log.time.strftime("%I:%M %p"),
                            "status": log.status
                        }
                        for log in login_logs
                    ],
                    "attendance": {
                        "month": attendance.month if attendance else None,
                        "present": attendance.present if attendance else 0,
                        "absent": attendance.absent if attendance else 0,
                        "total_days": attendance.total_days if attendance else 0
                    }
                },
                "message": "Rider monitoring details retrieved successfully"
            },
            status=status.HTTP_200_OK
        )
    
# rider rate filters 
class RiderRateFilterView(APIView):

    def get(self, request):

        rates = RiderRate.objects.filter(is_deleted=False)

        rider_types = list(
            rates.values_list("rider_type", flat=True).distinct()
        )

        zones = list(
            rates.values_list("zone", flat=True).distinct()
        )

        vehicles = list(
            rates.values_list("vehicle", flat=True).distinct()
        )

        statuses = list(
            rates.values_list("status", flat=True).distinct()
        )

        return Response({
            "status": True,
            "data": {
                
                "rider_types": ["All Rider Types"] + rider_types,
                "zones": ["All Zones"] + zones,
                "vehicles": ["All Vehicles"] + vehicles,
                "statuses": ["All statuses"] + statuses,
            },
            "message": "Rider rate filters retrieved successfully"
        })

class RiderOrderListView(APIView):

    @extend_schema(
        responses={200: RiderOrderSerializer(many=True)},
    )
    def get(self, request, rider_id):

        try:
            rider = Rider.objects.get(
                id=rider_id,
                is_deleted=False
            )
        except Rider.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "data": [],
                    "message": "Rider not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        orders = RiderOrder.objects.filter(
            rider=rider
        ).order_by("-order_date")

        serializer = RiderOrderSerializer(
            orders,
            many=True
        )

        return Response(
            {
                "status": True,
                "data": serializer.data,
                "message": "Rider orders retrieved successfully"
            },
            status=status.HTTP_200_OK
        )

class RiderEarningsPayoutView(APIView):

    @extend_schema(responses={200: RiderEarningsPayoutSerializer})
    def get(self, request, rider_id):
        try:
            rider = Rider.objects.get(
                id=rider_id,
                is_deleted=False
            )
        except Rider.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "data": {},
                    "message": "Rider not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RiderEarningsPayoutSerializer(rider)

        return Response(
            {
                "status": True,
                "data": serializer.data,
                "message": "Rider earnings and payout details retrieved successfully"
            },
            status=status.HTTP_200_OK
        )