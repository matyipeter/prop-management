from .models import Tenant, Property, PropertyManager
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class TenantRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Tenant.objects.create(user=user)
        return user

class PropertyManagerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            PropertyManager.objects.create(user=user)
        return user
    

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'city', 'state']


class TenantForm(forms.ModelForm):
    class Meta():
        model = Tenant
        fields = ['phone_number']


class ManagerForm(forms.ModelForm):
    class Meta():
        model = PropertyManager
        fields = ['phone_number']