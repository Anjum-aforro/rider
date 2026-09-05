from django.db import models

class Rider(models.Model):

    RIDER_TYPE_CHOICES = [
        ("Salary-based", "Salary-based"),
        ("Per-order", "Per-order"),
    ]

    PAYOUT_METHOD_CHOICES = [
        ("UPI", "UPI"),
        ("Bank Account", "Bank Account"),
    ]

    ACCOUNT_STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    ONLINE_STATUS_CHOICES = [
        ("Online", "Online"),
        ("Offline", "Offline"),
        ("On Break", "On Break"),
        ("On Delivery", "On Delivery"),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    rider_type = models.CharField(
        max_length=20,
        choices=RIDER_TYPE_CHOICES
    )

    assigned_store = models.CharField(max_length=100)
    assigned_zone = models.CharField(max_length=100)

    payout_method = models.CharField(
        max_length=20,
        choices=PAYOUT_METHOD_CHOICES
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

    driving_license_number = models.CharField(max_length=50)
    driving_license_document = models.URLField()

    aadhaar_number = models.CharField(max_length=20)
    aadhaar_document = models.URLField()

    vehicle_rc_number = models.CharField(max_length=50)
    vehicle_rc_document = models.URLField()

    account_status = models.CharField(
        max_length=20,
        choices=ACCOUNT_STATUS_CHOICES
    )

    activate_immediately = models.BooleanField()

    online_status = models.CharField(
        max_length=20,
        choices=ONLINE_STATUS_CHOICES,
        default="Offline"
    )

    current_order = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    cash_in_hand = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    has_undeposited_cash = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)