from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.EmailField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.EmailField(null=True, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f'DL0{self.id} ' + self.first_name + ' ' + self.last_name

class Retailer(models.Model):
    name = models.CharField(max_length=200, default='Default Retailer Name')
    address = models.TextField(default='Default Address')
    pincode = models.CharField(max_length=10, default='Default Pincode')
    contact_number = models.CharField(max_length=20, default='Default Contact Number')
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='retailers', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.EmailField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return  f'EMP0{self.id} ' + self.first_name + ' ' + self.last_name
