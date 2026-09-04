from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Rider
from .serializers import RiderSerializer


class RiderListView(APIView):
  def get(self, request):
    riders = Rider.objects.all()

    search = request.GET.get("search")

    if search:
        riders = riders.filter(name__icontains=search)

    vehicle_number = request.GET.get("vehicle_number")

    if vehicle_number:
        riders = riders.filter(vehicle_number__icontains=vehicle_number)

    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 10))

    start = (page - 1) * page_size
    end = start + page_size

    total_count = riders.count()
    riders = riders[start:end]

    serializer = RiderSerializer(riders, many=True)

    return Response({
        "status": True,
        "data": serializer.data,
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "message": "Riders retrieved successfully"
    })