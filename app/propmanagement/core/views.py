from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from core.models import Property, PropertyManager, Tenant
from django.views.generic import CreateView, View, ListView, UpdateView, DeleteView
from .forms import TenantRegistrationForm, PropertyManagerRegistrationForm, PropertyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
# Create your views here.

def index(request):
    properties = Property.objects.all()
    property_managers = PropertyManager.objects.all()
    tenants = Tenant.objects.all()

    context = {
        "properties": properties,
        "property_managers": property_managers,
        "tenants": tenants
    }

    
    return render(request, "core/index.html", context)


class TenantRegister(View):
    def get(self, request):
        form = TenantRegistrationForm()
        return render(request, 'registration/tenant_register.html', {'form': form})

    def post(self, request):
        form = TenantRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            tenant_group = Group.objects.get(name='Tenants')
            user.groups.add(tenant_group)
            return redirect('core:login')
        
class PropertyManagerRegister(View):
    def get(self, request):
        form = PropertyManagerRegistrationForm()
        return render(request, 'registration/property_manager_register.html', {'form': form})

    def post(self, request):
        form = PropertyManagerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            property_manager_group = Group.objects.get(name='Managers')
            user.groups.add(property_manager_group)
            return redirect('core:login')


@login_required
def dashboard(request):
    tenant = Tenant.objects.get(user=request.user)
    return render(request, 'core/tenant_dashboard.html', {'tenant': tenant})


@login_required
def logout_view(request):
    logout(request)
    return redirect('core:index')



# PROPETY MANAGER VIEWS, ADD, UPDATE, DELETE

class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'core/property_manager_dashboard.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(manager=self.request.user.propertymanager)


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'core/property_form.html'
    success_url = reverse_lazy('core:property_manager_dashboard')

    def form_valid(self, form):
        form.instance.manager = self.request.user.propertymanager
        return super().form_valid(form)

class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'core/property_form.html'
    success_url = reverse_lazy('core:property_manager_dashboard')

class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = 'core/property_confirm_delete.html'
    success_url = reverse_lazy('core:property_manager_dashboard')

#################################################################

