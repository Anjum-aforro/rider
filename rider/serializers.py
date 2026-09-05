from rest_framework import serializers

from .models import Rider, RiderDeposit


class RiderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rider
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "online_status",
            "current_order",
            "cash_in_hand",
            "has_undeposited_cash",
        ]

    # -------------------------
    # Phone validation
    # -------------------------
    def validate_phone(self, value):

        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return value

    # -------------------------
    # Complete rider validation
    # -------------------------
    def validate(self, attrs):

        rider_type = attrs.get(
            "rider_type",
            getattr(self.instance, "rider_type", None)
        )

        payout_method = attrs.get(
            "payout_method",
            getattr(self.instance, "payout_method", None)
        )

        # -------------------------
        # Basic required fields
        # -------------------------
        address = attrs.get(
            "address",
            getattr(self.instance, "address", None)
        )

        if not address:
            raise serializers.ValidationError({
                "address": "Address is required."
            })

        assigned_store = attrs.get(
            "assigned_store",
            getattr(self.instance, "assigned_store", None)
        )

        if not assigned_store:
            raise serializers.ValidationError({
                "assigned_store": "Assigned store is required."
            })

        assigned_zone = attrs.get(
            "assigned_zone",
            getattr(self.instance, "assigned_zone", None)
        )

        if not assigned_zone:
            raise serializers.ValidationError({
                "assigned_zone": "Assigned zone is required."
            })

        # -------------------------
        # Rider type validation
        # -------------------------
        if rider_type == Rider.RiderType.SALARY:

            base_salary = attrs.get(
                "base_salary",
                getattr(self.instance, "base_salary", None)
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
                getattr(self.instance, "per_order_rate", None)
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
        # Per KM rate
        # -------------------------
        per_km_rate = attrs.get(
            "per_km_rate",
            getattr(self.instance, "per_km_rate", None)
        )

        if per_km_rate is not None and per_km_rate < 0:
            raise serializers.ValidationError({
                "per_km_rate":
                    "Per-km rate cannot be negative."
            })

        # -------------------------
        # Payout method validation
        # -------------------------
        if payout_method == Rider.PayoutMethod.UPI:

            upi_id = attrs.get(
                "upi_id",
                getattr(self.instance, "upi_id", None)
            )

            if not upi_id:
                raise serializers.ValidationError({
                    "upi_id":
                        "UPI ID is required when payout method is UPI."
                })

        elif payout_method == Rider.PayoutMethod.BANK:

            bank_account = attrs.get(
                "bank_account_number",
                getattr(self.instance, "bank_account_number", None)
            )

            if not bank_account:
                raise serializers.ValidationError({
                    "bank_account_number":
                        "Bank account number is required when payout method is Bank Account."
                })

            ifsc = attrs.get(
                "ifsc_code",
                getattr(self.instance, "ifsc_code", None)
            )

            if not ifsc:
                raise serializers.ValidationError({
                    "ifsc_code":
                        "IFSC code is required when payout method is Bank Account."
                })

            holder = attrs.get(
                "account_holder_name",
                getattr(self.instance, "account_holder_name", None)
            )

            if not holder:
                raise serializers.ValidationError({
                    "account_holder_name":
                        "Account holder name is required when payout method is Bank Account."
                })

        return attrs


# =========================================================
# Rider COD Deposit Serializer
# =========================================================

class RiderDepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiderDeposit

        fields = [
            "id",
            "rider",
            "amount_received",
            "deposit_date",
            "notes",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "rider",
            "created_at",
        ]

    # -------------------------
    # Deposit amount validation
    # -------------------------
    def validate_amount_received(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Amount received must be greater than 0."
            )

        return value