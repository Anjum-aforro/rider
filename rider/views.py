from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Rider
from .serializers import RiderSerializer, RiderDepositSerializer


class RiderListView(APIView):

    @extend_schema(request=RiderSerializer)

    # POST /rider/
    def post(self, request):

        serializer = RiderSerializer(
            data=request.data
        )

        if serializer.is_valid():

            rider = serializer.save()

            return Response({   
                "status": True,
                "data": RiderSerializer(rider).data,
                "message": "Rider created successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors,
            "message": "Rider creation failed"
        }, status=status.HTTP_400_BAD_REQUEST)


class RiderDetailView(APIView):

    @extend_schema(request=RiderSerializer)    
    # PATCH /rider/<id>/
    def patch(self, request, id):

        try:
            rider = Rider.objects.get(id=id)

        except Rider.DoesNotExist:

            return Response({
                "status": False,
                "message": "Rider not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = RiderSerializer(
            rider,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            rider = serializer.save()

            return Response({
                "status": True,
                "data": RiderSerializer(rider).data,
                "message": "Rider updated successfully"
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "errors": serializer.errors,
            "message": "Rider update failed"
        }, status=status.HTTP_400_BAD_REQUEST)

    
    # DELETE /rider/<id>/
    def delete(self, request, id):

        try:
            rider = Rider.objects.get(id=id)

        except Rider.DoesNotExist:

            return Response({
                "status": False,
                "message": "Rider not found"
            }, status=status.HTTP_404_NOT_FOUND)

        rider.is_deleted = True
        rider.account_status = Rider.AccountStatus.INACTIVE
        rider.save(update_fields=["is_deleted", "account_status", "updated_at"])

        return Response({
            "status": True,
            "message": "Rider deleted successfully"
        }, status=status.HTTP_200_OK)





class RiderDepositView(APIView):
    # POST /rider/<id>/deposit/

    @extend_schema(request=RiderDepositSerializer)
    def post(self, request, id):

        try:
            rider = Rider.objects.get(
                id=id,
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

        serializer = RiderDepositSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": False,
                    "errors": serializer.errors,
                    "message": "Deposit failed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        amount_received = serializer.validated_data["amount_received"]

        # --------------------------------
        # Check available cash
        # --------------------------------
        if amount_received > rider.cash_in_hand:
            return Response(
                {
                    "status": False,
                    "message": (
                        "Deposit amount cannot be greater than "
                        "rider's cash in hand."
                    ),
                    "cash_in_hand": rider.cash_in_hand,
                    "amount_received": amount_received,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------
        # Create deposit and update rider
        # --------------------------------
        with transaction.atomic():

            deposit = RiderDeposit.objects.create(
                rider=rider,
                amount_received=amount_received,
                deposit_date=serializer.validated_data["deposit_date"],
                notes=serializer.validated_data.get("notes")
            )

            rider.cash_in_hand -= amount_received

            rider.has_undeposited_cash = rider.cash_in_hand > 0

            rider.save(
                update_fields=[
                    "cash_in_hand",
                    "has_undeposited_cash",
                    "updated_at"
                ]
            )

        return Response(
            {
                "status": True,
                "data": {
                    "deposit": RiderDepositSerializer(deposit).data,
                    "cash_in_hand": rider.cash_in_hand,
                    "has_undeposited_cash": rider.has_undeposited_cash,
                },
                "message": "COD deposit confirmed successfully"
            },
            status=status.HTTP_201_CREATED
        )