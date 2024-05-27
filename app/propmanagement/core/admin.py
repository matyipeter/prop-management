from django.contrib import admin
from core.models import Property, PropertyManager, Tenant

admin.site.register(Property)
admin.site.register(PropertyManager)
admin.site.register(Tenant)

