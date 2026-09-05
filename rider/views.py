from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import Rider
from .serializers import RiderSerializer


class RiderListView(APIView):
    """
    POST /rider/

    Creates a new rider.

    GET is intentionally NOT implemented because
    Rider GET is handled by another teammate.
    """

    @extend_schema(
        request=RiderSerializer,
        responses={201: RiderSerializer},
    )
    def post(self, request):

        serializer = RiderSerializer(
            data=request.data
        )

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
    PATCH /rider/<id>/
    DELETE /rider/<id>/

    GET is intentionally NOT implemented.
    """

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

        # Soft delete / deactivate rider.
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