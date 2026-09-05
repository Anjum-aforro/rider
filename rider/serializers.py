from rest_framework import serializers
from .models import Rider

class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = [
            "name",
            "rider_type",
             "phone",
            "assigned_store",
            "assigned_zone",
            "online_status",
            "current_order",
            "cash_in_hand",
            "account_status"
        ]