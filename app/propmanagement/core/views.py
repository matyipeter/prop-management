from django.shortcuts import render, redirect
from core.models import Property, Property_Manager, Tenant
from django.views.generic import CreateView, View
from .forms import RegistrationForm, TenantForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group
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
            tenant_group = Group.objects.get(name='Tenants')
            user.groups.add(tenant_group)
            user.save()
            tenant = tenant_form.save(commit=False)
            tenant.user = user
            tenant.save()
            return redirect('/')  # Redirect to the home page after successful registration
        
        return render(request, 'core/register.html', {'form': form, 'tenantform':tenant_form})  # Render the registration template with the form



@login_required
def dashboard(request):
    tenant = Tenant.objects.get(user=request.user)
    return render(request, 'core/dashboard.html', {'tenant': tenant})

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:index')


class AddProperty(CreateView):
    model = Property
    fields = '__all__'
