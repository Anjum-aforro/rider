from django.db import models


class RiderRate(models.Model):

    class RateType(models.TextChoices):
        PER_KM = "Per KM", "Per KM"
        FIXED = "Fixed", "Fixed"

    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    distance_from = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    distance_to = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    base_payout = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    per_km_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    rider_type = models.CharField(
        max_length=20
    )

    zone = models.CharField(
        max_length=100
    )

    vehicle = models.CharField(
        max_length=100
    )

    rate_type = models.CharField(
        max_length=20,
        choices=RateType.choices
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    is_deleted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.distance_from} - {self.distance_to} KM"