from django.utils import timezone
from datetime import timedelta
from rider.models import (
    Rider,
    RiderCurrentAssignment,
    RiderLoginLogoutLog,
    RiderAttendance,
    RiderOrder,
    RiderDeposit,
    RiderPayout,
    RiderIncentive,
    RiderActivityLog,
    RiderSalaryHistory,
)

rider, created = Rider.objects.get_or_create(
    phone="9999900001",
    defaults={
        "name": "Test Rider",
        "email": "testrider@example.com",
        "address": "Bengaluru, Karnataka",
        "rider_type": "Salary-based",
        "base_salary": 15000,
        "per_order_rate": 0,
        "per_km_rate": 10,
        "assigned_store": "Test Store",
        "assigned_zone": "Bengaluru",
        "payout_method": "UPI",
        "upi_id": "testrider@upi",
        "driving_license_number": "DL-TEST-0001",
        "aadhaar_number": "XXXX-XXXX-0001",
        "vehicle_rc_number": "RC-TEST-0001",
        "account_status": "Active",
        "activate_immediately": True,
        "is_deleted": False,
    },
)

rider.online_status = "Online"
rider.cash_in_hand = 4850
rider.has_undeposited_cash = True
rider.total_orders_delivered = 25
rider.average_rating = 4.8
rider.completion_rate = 95
rider.total_earnings = 37500
rider.save()

RiderCurrentAssignment.objects.update_or_create(
    rider=rider,
    defaults={
        "order_id": "ORD-TEST-1001",
        "status": "On Delivery",
        "pickup": "Test Store, Bengaluru",
        "drop": "Customer Address, Bengaluru",
        "customer": "Test Customer",
        "order_value": 750,
    },
)

RiderLoginLogoutLog.objects.get_or_create(
    rider=rider,
    time__date=timezone.now().date(),
    status="Login",
    defaults={"time": timezone.now()},
)

RiderAttendance.objects.update_or_create(
    rider=rider,
    month="May 2024",
    defaults={
        "present": 25,
        "absent": 2,
        "total_days": 27,
    },
)

RiderOrder.objects.get_or_create(
    rider=rider,
    order_id="ORD-TEST-1001",
    defaults={
        "order_date": timezone.now() - timedelta(days=1),
        "status": "Delivered",
        "order_value": 450,
        "delivery_time": "35 mins",
        "customer_rating": 4.8,
    },
)

RiderOrder.objects.get_or_create(
    rider=rider,
    order_id="ORD-TEST-1002",
    defaults={
        "order_date": timezone.now() - timedelta(days=2),
        "status": "Delivered",
        "order_value": 650,
        "delivery_time": "40 mins",
        "customer_rating": 4.9,
    },
)

RiderOrder.objects.get_or_create(
    rider=rider,
    order_id="ORD-TEST-1003",
    defaults={
        "order_date": timezone.now() - timedelta(days=3),
        "status": "Pending",
        "order_value": 550,
        "delivery_time": "30 mins",
        "customer_rating": None,
    },
)

RiderPayout.objects.get_or_create(
    rider=rider,
    amount_paid=5000,
    payment_mode="UPI",
    payout_date=timezone.now().date(),
    defaults={"notes": "Weekly payout"},
)

RiderPayout.objects.get_or_create(
    rider=rider,
    amount_paid=4500,
    payment_mode="Bank Transfer",
    payout_date=timezone.now().date() - timedelta(days=7),
    defaults={"notes": "Weekly payout"},
)

RiderPayout.objects.get_or_create(
    rider=rider,
    amount_paid=3000,
    payment_mode="Cash",
    payout_date=timezone.now().date() - timedelta(days=14),
    defaults={"notes": "Cash payout"},
)

RiderSalaryHistory.objects.get_or_create(
    rider=rider,
    month="May 2024",
    defaults={
        "amount": 15000,
        "status": "Completed",
    },
)

RiderSalaryHistory.objects.get_or_create(
    rider=rider,
    month="April 2024",
    defaults={
        "amount": 15000,
        "status": "Completed",
    },
)

RiderDeposit.objects.get_or_create(
    rider=rider,
    amount_received=4850,
    deposit_date=timezone.now().date(),
    defaults={"notes": "COD cash deposited"},
)

RiderDeposit.objects.get_or_create(
    rider=rider,
    amount_received=5230,
    deposit_date=timezone.now().date() - timedelta(days=3),
    defaults={"notes": "COD cash deposited"},
)

RiderDeposit.objects.get_or_create(
    rider=rider,
    amount_received=4600,
    deposit_date=timezone.now().date() - timedelta(days=6),
    defaults={"notes": "COD cash deposited"},
)

RiderIncentive.objects.get_or_create(
    rider=rider,
    target="50 Deliveries Goal",
    defaults={
        "requirement": "50 deliveries",
        "progress": "25 / 50",
        "remaining": "25 deliveries left",
        "description": "Complete 50 deliveries",
        "rating": None,
        "reward": 500,
        "status": "Active",
    },
)

RiderIncentive.objects.get_or_create(
    rider=rider,
    target="Rating Bonus",
    progress="4.85 / 4.80",
    defaults={
        "requirement": "4.80+ rating",
        "remaining": "Completed",
        "description": "Maintain 4.80+ average rating",
        "rating": 4.85,
        "reward": 500,
        "status": "Completed",
    },
)

activities = [
    "Order #ORD-TEST-1001 marked as Delivered",
    "Rider went Online",
    "Cash deposit of ₹4,850 completed",
    "Document Driving License updated",
    "Rider went Offline",
]

for index, activity in enumerate(activities):
    RiderActivityLog.objects.get_or_create(
        rider=rider,
        activity=activity,
        defaults={
            "date_time": timezone.now() - timedelta(days=index)
        },
    )

print("Dummy Rider data created successfully.")
print("Rider ID:", rider.id)
print("Phone:", rider.phone)
print("Use this Rider ID to test the Rider APIs.")