from django import forms
from django.db.models import fields
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class CreateCustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'input'}),
            'name': forms.TextInput(attrs={'class': 'input'}),
            'password': forms.PasswordInput()
        }

        labels = {
            'email': 'E-mail',
            'name': 'Name',
            'password': 'Password',
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UpdateCustomUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        
        user = self.request.user
        self.user_rol = self.get_user_rol(user)
        print(self.user_rol)
        if self.user_rol != 'Boss' or self.instance.status != 1:
            self.fields['email'].widget.attrs['class'] = 'disable'
            self.fields['name'].widget.attrs['class'] = 'disable'
            self.fields['rol'].widget.attrs['class'] = 'disable'
            self.fields['status'].widget.attrs['class'] = 'disable'
            self.fields['description'].widget.attrs['class'] = 'disable'

    def get_user_rol(self, user):
        return user.groups.all().values_list('name')[0][0]

    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if self.user_rol != 'Boss' or instance.status != 1:
            return instance.email
        else:
            return self.cleaned_data['email']

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if self.user_rol != 'Boss' or instance.status != 1:
            return instance.name
        else:
            return self.cleaned_data['name']

    def clean_rol(self):
        instance = getattr(self, 'instance', None)
        if self.user_rol != 'Boss' or instance.status != 1:
            return instance.rol
        else:
            return self.cleaned_data['rol']

    def clean_status(self):
        instance = getattr(self, 'instance', None)
        if self.user_rol != 'Boss' or instance.status != 1:
            return instance.status
        else:
            return self.cleaned_data['status']
    
    def clean_description(self):
        instance = getattr(self, 'instance', None)
        if self.user_rol != 'Boss' or instance.status != 1:
            return instance.description
        else:
            return self.cleaned_data['description']

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'rol', 'status', 'description']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'input'}),
            'name': forms.TextInput(attrs={'class': 'input'}),
            'rol': forms.Select(),
            'status': forms.Select(),
            'description': forms.Textarea(attrs={'class': 'input'}),
        }

        labels = {
            'email': 'E-mail',
            'name': 'Name',
            'rol': 'Rol',
            'status': 'Status',
            'description': 'Description',
        }