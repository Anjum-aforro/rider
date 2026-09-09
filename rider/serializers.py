import re
from rest_framework import serializers
from .models import Rider, RiderActivityLog, RiderIncentive, RiderRate
from .models import (
  Rider, 
  RiderCurrentAssignment, 
  RiderLoginLogoutLog,
  RiderAttendance,
  RiderOrder,
  RiderPayout
  )



class RiderSerializer(serializers.ModelSerializer):
    """
    Serializer used only by Rider POST and PATCH APIs.
    GET APIs are intentionally not implemented here.
    """

    # Explicit file upload fields
    driving_license_document = serializers.FileField(
        required=True
    )

    aadhaar_document = serializers.FileField(
        required=True
    )

    vehicle_rc_document = serializers.FileField(
        required=True
    )

    class Meta:
        model = Rider

        fields = [
             "id",
             "name",
             "email",
             "phone",
             "address",
             "rider_type",
             "base_salary",
             "per_order_rate",
             "per_km_rate",
             "assigned_store",
             "assigned_zone",
             "payout_method",
             "upi_id",
             "bank_account_number",
             "ifsc_code",
             "account_holder_name",
             "driving_license_number",
             "driving_license_document",
             "driving_license_verification_status",
             "aadhaar_number",
             "aadhaar_document",
             "aadhaar_verification_status",
             "vehicle_rc_number",
             "vehicle_rc_document",
             "vehicle_rc_verification_status",
             "account_status",
             "is_deleted",
             "activate_immediately",
             "online_status",
             "current_order",
             "cash_in_hand",
             "has_undeposited_cash",
             "vehicle_number",
             "created_at",
             "updated_at",
]

        read_only_fields = [
            "id",
            "online_status",
            "current_order",
            "cash_in_hand",
            "has_undeposited_cash",
            "created_at",
        ]

        extra_kwargs = {
            "name": {
                "required": True,
            },
            "phone": {
                "required": True,
            },
            "address": {
                "required": True,
            },
            "rider_type": {
                "required": True,
            },
            "assigned_store": {
                "required": True,
            },
            "assigned_zone": {
                "required": True,
            },
            "payout_method": {
                "required": True,
            },
            "driving_license_number": {
                "required": True,
            },
            "aadhaar_number": {
                "required": True,
            },
            "vehicle_rc_number": {
                "required": True,
            },
            "account_status": {
                "required": False,
            },
            "activate_immediately": {
                "required": True,
            },
        }

    # -------------------------
    # PHONE VALIDATION
    # -------------------------
    def validate_phone(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return value

    # -------------------------
    # FILE VALIDATION
    # -------------------------
    def validate_document_file(self, value, field_name):
        if value is None:
            return value

        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
        ]

        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                f"{field_name} must be a PDF, JPG, or PNG file."
            )

        max_size = 5 * 1024 * 1024  # 5 MB

        if value.size > max_size:
            raise serializers.ValidationError(
                f"{field_name} must not exceed 5 MB."
            )

        return value

    def validate_driving_license_document(self, value):
        return self.validate_document_file(
            value,
            "Driving licence document",
        )

    def validate_aadhaar_document(self, value):
        return self.validate_document_file(
            value,
            "Aadhaar document",
        )

    def validate_vehicle_rc_document(self, value):
        return self.validate_document_file(
            value,
            "Vehicle RC document",
        )

    # -------------------------
    # COMPLETE RIDER VALIDATION
    # -------------------------
    def validate(self, attrs):
        if self.instance is None:
            driving_license_number = attrs.get("driving_license_number")
            vehicle_number = attrs.get("vehicle_number")

            if Rider.objects.filter(
                driving_license_number=driving_license_number,
                is_deleted=False
            ).exists():
                raise serializers.ValidationError({
                    "driving_license_number":
                        "Driving licence number already exists."
                })

            if Rider.objects.filter(
                vehicle_number=vehicle_number,
                is_deleted=False
            ).exists():
                raise serializers.ValidationError({
                    "vehicle_number":
                        "Vehicle number already exists."
                })
                driving_license_number = attrs.get("driving_license_number")
        vehicle_number = attrs.get("vehicle_number")


        # Existing values are used for PATCH.
        rider_type = attrs.get(
            "rider_type",
            getattr(self.instance, "rider_type", None),
        )

        payout_method = attrs.get(
            "payout_method",
            getattr(self.instance, "payout_method", None),
        )

        address = attrs.get(
            "address",
            getattr(self.instance, "address", None),
        )

        assigned_store = attrs.get(
            "assigned_store",
            getattr(self.instance, "assigned_store", None),
        )

        assigned_zone = attrs.get(
            "assigned_zone",
            getattr(self.instance, "assigned_zone", None),
        )

        # -------------------------
        # REQUIRED BASIC FIELDS
        # -------------------------
        if not address:
            raise serializers.ValidationError({
                "address": "Address is required."
            })

        if not assigned_store:
            raise serializers.ValidationError({
                "assigned_store": "Assigned store is required."
            })

        if not assigned_zone:
            raise serializers.ValidationError({
                "assigned_zone": "Assigned zone is required."
            })

        # -------------------------
        # RIDER TYPE
        # -------------------------
        if rider_type == Rider.RiderType.SALARY:

            base_salary = attrs.get(
                "base_salary",
                getattr(self.instance, "base_salary", None),
            )

            if base_salary is None:
                raise serializers.ValidationError({
                    "base_salary":
                        "Base salary is required for salary-based riders."
                })

            if base_salary < 0:
                raise serializers.ValidationError({
                    "base_salary":
                        "Base salary cannot be negative."
                })

        elif rider_type == Rider.RiderType.PER_ORDER:

            per_order_rate = attrs.get(
                "per_order_rate",
                getattr(self.instance, "per_order_rate", None),
            )

            if per_order_rate is None:
                raise serializers.ValidationError({
                    "per_order_rate":
                        "Per-order rate is required for per-order riders."
                })

            if per_order_rate < 0:
                raise serializers.ValidationError({
                    "per_order_rate":
                        "Per-order rate cannot be negative."
                })

        # -------------------------
        # PER-KM RATE
        # -------------------------
        per_km_rate = attrs.get(
            "per_km_rate",
            getattr(self.instance, "per_km_rate", None),
        )

        if per_km_rate is not None and per_km_rate < 0:
            raise serializers.ValidationError({
                "per_km_rate":
                    "Per-km rate cannot be negative."
            })

        # -------------------------
        # PAYOUT METHOD
        # -------------------------
        if payout_method == Rider.PayoutMethod.UPI:

            upi_id = attrs.get(
                "upi_id",
                getattr(self.instance, "upi_id", None),
            )

            if not upi_id:
                raise serializers.ValidationError({
                    "upi_id":
                        "UPI ID is required when payout method is UPI."
                })

        elif payout_method == Rider.PayoutMethod.BANK:

            bank_account_number = attrs.get(
                "bank_account_number",
                getattr(self.instance, "bank_account_number", None),
            )

            if not bank_account_number:
                raise serializers.ValidationError({
                    "bank_account_number":
                        "Bank account number is required "
                        "when payout method is Bank Account."
                })

            ifsc_code = attrs.get(
                "ifsc_code",
                getattr(self.instance, "ifsc_code", None),
            )

            if not ifsc_code:
                raise serializers.ValidationError({
                    "ifsc_code":
                        "IFSC code is required "
                        "when payout method is Bank Account."
                })

            account_holder_name = attrs.get(
                "account_holder_name",
                getattr(self.instance, "account_holder_name", None),
            )

            if not account_holder_name:
                raise serializers.ValidationError({
                    "account_holder_name":
                        "Account holder name is required "
                        "when payout method is Bank Account."
                })

        return attrs


class RiderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rider

        fields = [
            "id",
            "name",
            "phone",
            "rider_type",
            "assigned_store",
            "assigned_zone",
            "online_status",
            "current_order",
            "cash_in_hand",
            "account_status",
        ]


class LegacyRiderRateSerializer(serializers.ModelSerializer):

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
            "created_at",
            "updated_at"
]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class RiderRateGetSerializer(serializers.ModelSerializer):

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
            "is_deleted",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

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
            "rate_type",
            "zone",
            "vehicle",
            "status",
        ]


class RiderCurrentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderCurrentAssignment
        fields = [
            "order_id",
            "status",
            "pickup",
            "drop",
            "customer",
            "order_value"
        ]


class RiderLoginLogoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderLoginLogoutLog
        fields = [
            "time",
            "status"
        ]


class RiderAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderAttendance
        fields = [
            "month",
            "present",
            "absent",
            "total_days"
        ]

class RiderOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiderOrder
        fields = [
            "order_id",
            "order_date",
            "status",
            "order_value",
            "delivery_time",
            "customer_rating"
        ]

class RiderEarningsPayoutSerializer(serializers.Serializer):
    payout_history = serializers.SerializerMethodField()
    salary_details = serializers.SerializerMethodField()
    salary_history = serializers.SerializerMethodField()

    def get_payout_history(self, obj):
        return [
            {
                "amount_paid": f"₹{payout.amount_paid:,.2f}",
                "payment_mode": payout.payment_mode,
                "payout_date": payout.payout_date,
                "notes": payout.notes
            }
            for payout in obj.payouts.all().order_by("-payout_date")
        ]

    def get_salary_details(self, obj):
        return {
            "monthly_salary": f"₹{obj.base_salary:,.0f}" if obj.base_salary else "₹0",
            "this_month": f"₹{obj.base_salary:,.0f}" if obj.base_salary else "₹0",
            "next_payout": "31 May 2024"
        }

    def get_salary_history(self, obj):
        return [
        {
            "month": salary.month,
            "amount": f"₹{salary.amount:,.0f}",
            "status": salary.status
        }
        for salary in obj.salary_history.all().order_by("-paid_date")
    ]

class RiderCODSerializer(serializers.Serializer):
    cod_summary = serializers.SerializerMethodField()
    cash_collected_per_order = serializers.SerializerMethodField()
    deposit_history = serializers.SerializerMethodField()

    def get_cod_summary(self, obj):
        return {
            "total_cash_in_hand": f"₹{obj.cash_in_hand:,.2f}",
            "last_updated": obj.updated_at.strftime("%I:%M %p"),
            "total_collected_today": "₹3,750",
            "total_pending_deposit": f"₹{obj.cash_in_hand:,.2f}"
        }

    def get_cash_collected_per_order(self, obj):
        return [
            {
                "order_id": f"#{order.order_id}",
                "collected_amount": f"₹{order.order_value:,.0f}",
                "status": "Pending"
            }
            for order in obj.orders.all().order_by("-order_date")
        ]

    def get_deposit_history(self, obj):
        return [
            {
                "date": deposit.deposit_date.strftime("%d %B %Y"),
                "amount": f"₹{deposit.amount_received:,.0f}",
                "reference": f"DEP{deposit.id:05d}",
                "status": "Completed"
            }
            for deposit in obj.deposits.all().order_by("-deposit_date")
        ]

class RiderIncentiveSerializer(serializers.ModelSerializer):
    reward = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = RiderIncentive
        fields = [
            "target",
            "requirement",
            "progress",
            "remaining",
            "description",
            "rating",
            "reward",
            "status"
        ]

    def get_reward(self, obj):
        return f"₹{obj.reward:,.2f}"

    def get_rating(self, obj):
        return f"{obj.rating:.2f}" if obj.rating is not None else None

class RiderActivityLogSerializer(serializers.ModelSerializer):
    date_time = serializers.SerializerMethodField()

    class Meta:
        model = RiderActivityLog
        fields = ["activity", "date_time"]

    def get_date_time(self, obj):
        return obj.date_time.strftime("%d %B %Y, %I:%M %p")