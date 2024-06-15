from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Tenant(models.Model):

    # PERSONAL INFORMATION
    user = models.OneToOneField(User,verbose_name='user' ,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(default="2000-01-01", blank=False)
    rent = models.IntegerField(default=0)
    payment_status = models.BooleanField(default=False)

    # TIMESTAMPS
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class PropertyManager(models.Model):
    user = models.OneToOneField(User,verbose_name='user' ,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
    
    def number_of_properties(self):
        return self.properties.count()
    
    

class Property(models.Model):
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE, related_name='properties')
    tenant = models.ManyToManyField(Tenant, related_name='properties', blank=True, null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50, default="00000")

    def __str__(self):
        return self.name
    
    def no_of_tenants(self):
        return self.tenant.count()


class MaintananceRequests(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintanance_requests')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='maintanance_requests', blank=True, null=True)
    typ = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Request by {self.tenant.user.username} for {self.prop.name}"
