from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Rider
from .serializers import RiderSerializer, RiderListSerializer


class RiderListView(APIView):

    parser_classes = [MultiPartParser, FormParser]

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
        ]
    )
    def get(self, request):
        riders = Rider.objects.filter(is_deleted=False)

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

    def get(self, request):
        riders = Rider.objects.filter(is_deleted=False)

        total_fleet = riders.filter(
            account_status=Rider.AccountStatus.ACTIVE
        ).count()

        active_online = riders.filter(
            online_status=Rider.OnlineStatus.ONLINE
        ).count()

        on_delivery = riders.filter(
            online_status=Rider.OnlineStatus.ON_DELIVERY
        ).count()

        total_cash_in_hand = sum(
            rider.cash_in_hand for rider in riders
        )

        return Response(
            {
                "status": True,
                "data": {
                    "total_fleet": f"{total_fleet} Riders",
                    "active_online": f"{active_online} online now",
                    "on_delivery": f"{on_delivery} orders active",
                    "total_cash_in_hand": f"₹{total_cash_in_hand:,.0f}",
                },
                "message": "Rider stats retrieved successfully",
            }
        )


class RiderDetailView(APIView):

    parser_classes = [MultiPartParser, FormParser]

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
                "data": serializer.data,
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

    def get(self, request):
        return Response({
            "status": True,
            "data": {
                "rider_type": [
                    "Salary-based",
                    "Per-order"
                ],
                "assigned_store": [
                     "BTM Layout Stage 2",
                     "Bellandur Outer Ring",
                     "HSR Layout Sector 2",
                     "Indiranagar Darkstore",
                     "Jayanagar 4th Block",
                     "Koramangala Hub",
                     "Malleswaram Central",
                     "Whitefield Depot"
                ],
                "account_status": [
                    "Active",
                    "Inactive",
                    "Block",
                    "Pending",
                    "Suspend",
                    "Rejected"
                ]
            }
        })