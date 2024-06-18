from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "core"

urlpatterns = [

    path("", views.index, name="index"),
    path("register/tenant", views.TenantRegister.as_view(), name="tenant_register"),
    path("tenant/update/<int:pk>/", views.TenantUpdateView.as_view(), name="tenant_update"),
    path("register/property_manager", views.PropertyManagerRegister.as_view(), name="property_manager_register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("tenant-dashboard/", views.dashboard, name="tenant_dashboard"),
    path('property-manager-dashboard/', views.PropertyListView.as_view(), name='property_manager_dashboard'),
    path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('property/add/', views.PropertyCreateView.as_view(), name='add_property'),
    path('property/edit/<int:pk>/', views.PropertyUpdateView.as_view(), name='edit_property'),
    path('property/delete/<int:pk>/', views.PropertyDeleteView.as_view(), name='delete_property'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    #path('profile/<int:pk>', views.PropertyManagerProfileView.as_view(), name='property_manager_profile'),
    path('maintanance-request/add/', views.MaintananceRequestCreateView.as_view(), name='add_maintanance_request'),
]