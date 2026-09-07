from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema

from .models import Rider
from .serializers import RiderSerializer


class RiderListView(APIView):
    """
    GET /rider/
    POST /rider/

    GET supports search, filters and pagination.
    POST creates a new rider.
    """

    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        riders = Rider.objects.filter(is_deleted=False)

        search = request.GET.get("search")

        if search:
            riders = riders.filter(
                Q(name__icontains=search)
                | Q(assigned_store__icontains=search)
                | Q(current_order__icontains=search)
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

        if cash_filter == "above_10":
            riders = riders.filter(cash_in_hand__gt=10)

        elif cash_filter == "below_10":
            riders = riders.filter(cash_in_hand__lte=10)

        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))

        total_count = riders.count()

        start = (page - 1) * page_size
        end = start + page_size

        riders = riders[start:end]

        serializer = RiderSerializer(riders, many=True)

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


class RiderDetailView(APIView):
    """
    GET /rider/<id>/
    PATCH /rider/<id>/
    DELETE /rider/<id>/
    """

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