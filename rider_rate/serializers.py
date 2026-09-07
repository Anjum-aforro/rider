from rest_framework import serializers
from .models import RiderRate


class RiderRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiderRate
        fields = [
            "id",
            "distance_from",
            "distance_to",
            "base_payout",
            "per_km_rate",
            "rider_type",
            "zone",
            "vehicle",
            "rate_type",
            "status",
            "created_at",
            "updated_at",
        ]