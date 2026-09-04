from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Rider
from .serializers import RiderSerializer


class RiderListView(APIView):

    def get(self, request):
        rider = Rider.objects.all()
        serializer = RiderSerializer(rider, many=True)

        return Response({
            "status": True,
            "data": serializer.data,
            "message": "Riders retrieved successfully"
        })