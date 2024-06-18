from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from core.models import Property, PropertyManager, Tenant, MaintananceRequests
from django.views.generic import CreateView, View, ListView, UpdateView, DeleteView, DetailView
from .forms import TenantRegistrationForm, PropertyManagerRegistrationForm, PropertyForm, MaintananceRequestForm, TenantForm, PropertyManagerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
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
        
class TenantUpdateView(LoginRequiredMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'registration/tenant_details.html'
    success_url = reverse_lazy('core:tenant_dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self):
        return self.request.user.tenant


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
    

class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'core/property_detail.html'
    context_object_name = 'property'

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
@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.groups.filter(name='Managers').exists():
        u = PropertyManager.objects.get(user=user)
        template = 'core/property_manager_profile.html'
    elif user.groups.filter(name='Tenants').exists():
        u = Tenant.objects.get(user=user)
        template = 'core/tenant_profile_details.html'
    else:
        return redirect('core:login')
    return render(request, template, {'u': u})
        
#################################################################

class MaintananceRequestCreateView(LoginRequiredMixin, CreateView):
    model = MaintananceRequests
    form_class = MaintananceRequestForm
    template_name = 'core/m_request_form.html'
    success_url = reverse_lazy('core:tenant_dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)