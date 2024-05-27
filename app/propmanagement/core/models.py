from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tenant(models.Model):
    user = models.OneToOneField(User,verbose_name='user' ,on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True, default=0)
    date_of_birth = models.DateField(default="2000-01-01", blank=False)
    rent = models.IntegerField(default=0)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class PropertyManager(models.Model):
    user = models.OneToOneField(User,verbose_name='user' ,on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.user.username
    
    def number_of_properties(self):
        return self.properties.count()
    
    

class Property(models.Model):
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE, related_name='properties')
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, related_name='properties', blank=True, null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name