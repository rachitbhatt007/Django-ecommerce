from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile")
    mobilephone = models.CharField(max_length=15, unique=True)
    address = models.ForeignKey(
        'Address', related_name="address", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="myaddress")
    user_address = models.TextField(max_length=300)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user_address
