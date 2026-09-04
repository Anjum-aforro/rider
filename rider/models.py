from django.db import models

# Create your models here.

class Rider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
