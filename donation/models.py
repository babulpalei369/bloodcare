from django.db import models
from django.contrib.auth.models import User

BLOOD_GROUP_CHOICES = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units = models.PositiveIntegerField()
    donation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group} ({self.units} units)"

class BloodRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units = models.PositiveIntegerField()
    reason = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group} ({self.units} units)"

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name



