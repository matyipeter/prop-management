from django.shortcuts import render, redirect
from core.models import Property, Property_Manager, Tenant
from django.views.generic import CreateView, View
from .forms import RegistrationForm, TenantForm
# Create your views here.

def index(request):
    properties = Property.objects.all()
    property_managers = Property_Manager.objects.all()
    tenants = Tenant.objects.all()

    context = {
        "properties": properties,
        "property_managers": property_managers,
        "tenants": tenants
    }

    
    return render(request, "core/index.html", context)


class Register(View):
    def get(self, request):
        form = RegistrationForm()
        tenant_form = TenantForm()
        return render(request, 'core/register.html', {'form': form, 'tenantform':tenant_form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)  # Instantiate the user creation form with the posted data
        tenant_form = TenantForm(request.POST)
        # Check if the form data is valid
        if form.is_valid() and tenant_form.is_valid():
            user = form.save(commit=False)
            user.save()
            tenant = tenant_form.save(commit=False)
            tenant.user = user
            tenant.save()
            return redirect('/')  # Redirect to the home page after successful registration
        
        return render(request, 'core/register.html', {'form': form, 'tenantform':tenant_form})  # Render the registration template with the form