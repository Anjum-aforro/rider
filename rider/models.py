from django.db import models


class Rider(models.Model):

    class RiderType(models.TextChoices):
        SALARY = "Salary-based", "Salary-based"
        PER_ORDER = "Per-order", "Per-order"

    class PayoutMethod(models.TextChoices):
        UPI = "UPI", "UPI"
        BANK = "Bank Account", "Bank Account"

    class AccountStatus(models.TextChoices):
        ACTIVE = "Active", "Active"
        INACTIVE = "Inactive", "Inactive"

    class OnlineStatus(models.TextChoices):
        ONLINE = "Online", "Online"
        OFFLINE = "Offline", "Offline"
        ON_BREAK = "On Break", "On Break"
        ON_DELIVERY = "On Delivery", "On Delivery"

    # -------------------------
    # Basic information
    # -------------------------
    name = models.CharField(max_length=100)

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=10,
        unique=True
    )

    address = models.TextField()

    # -------------------------
    # Rider type
    # -------------------------
    rider_type = models.CharField(
        max_length=20,
        choices=RiderType.choices
    )

    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    per_order_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    per_km_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # -------------------------
    # Store / Zone assignment
    # -------------------------
    assigned_store = models.CharField(
        max_length=100
    )

    assigned_zone = models.CharField(
        max_length=100
    )

    # -------------------------
    # Payout information
    # -------------------------
    payout_method = models.CharField(
        max_length=20,
        choices=PayoutMethod.choices
    )

    upi_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    bank_account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    ifsc_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    account_holder_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # -------------------------
    # Documents
    # -------------------------
    driving_license_number = models.CharField(
        max_length=50
    )

    driving_license_document = models.FileField(
        upload_to="riders/driving_license/",
        blank=True,
        null=True
    )

    aadhaar_number = models.CharField(
        max_length=12,
        null=True,
        blank=True
    )

    aadhaar_document = models.FileField(
        upload_to="riders/aadhaar/",
        blank=True,
        null=True
    )

    vehicle_rc_number = models.CharField(
        max_length=50
    )

    vehicle_rc_document = models.FileField(
        upload_to="riders/vehicle_rc/",
        blank=True,
        null=True
    )

    # -------------------------
    # Account status
    # -------------------------
    account_status = models.CharField(
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.INACTIVE
    )

    is_deleted = models.BooleanField(
        default=False
    )

    activate_immediately = models.BooleanField(
        default=False
    )

    # -------------------------
    # Live / monitoring state
    # -------------------------
    online_status = models.CharField(
        max_length=20,
        choices=OnlineStatus.choices,
        default=OnlineStatus.OFFLINE
    )

    current_order = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # -------------------------
    # COD / cash
    # -------------------------
    cash_in_hand = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    has_undeposited_cash = models.BooleanField(
        default=False
    )

    # -------------------------
    # Vehicle
    # -------------------------
    # Kept from your existing model.
    vehicle_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # -------------------------
    # Timestamps
    # -------------------------
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} - {self.phone}"


class RiderDeposit(models.Model):

    rider = models.ForeignKey(
        Rider,
        on_delete=models.CASCADE,
        related_name="deposits"
    )

    amount_received = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    deposit_date = models.DateField()

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.rider.name} - ₹{self.amount_received}"