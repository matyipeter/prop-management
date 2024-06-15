from .models import Tenant, Property, PropertyManager, MaintananceRequests
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class TenantRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Email'
            }),
        }

    def clean(self):
        cleaned_data = super(TenantRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Tenant.objects.create(user=user)
        return user

class PropertyManagerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Email'
            }),
        }

    def clean(self):
        cleaned_data = super(PropertyManagerRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            PropertyManager.objects.create(user=user)
        return user
    

class MaintananceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintananceRequests
        fields = ['prop', 'typ','description']

        widgets = {
            'prop': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            }),
            'typ': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            }),
            'description': forms.Textarea(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Description',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MaintananceRequestForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['prop'].queryset = Property.objects.filter(tenant=user.tenant)

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'city', 'state']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Property Name'
            }),
            'address': forms.Textarea(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Address',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Price'
            }),
            'state': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'state'
            }),
        }


class TenantForm(forms.ModelForm):
    class Meta():
        model = Tenant
        fields = ['phone_number']


class ManagerForm(forms.ModelForm):
    class Meta():
        model = PropertyManager
        fields = ['phone_number']