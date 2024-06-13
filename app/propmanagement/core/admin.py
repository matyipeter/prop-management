from django.contrib import admin
from core.models import Property, PropertyManager, Tenant, MaintananceRequests

admin.site.register(Property)
admin.site.register(PropertyManager)
admin.site.register(MaintananceRequests)

class TenantAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user')

admin.site.register(Tenant, TenantAdmin)

