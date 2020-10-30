from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=10, null=False, unique=True)
    address = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    city = models.CharField(max_length=50)
    amount = models.IntegerField(null=False)
    customerId = models.CharField(max_length=200, null=False)
    multi_use_payment_token = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.id



