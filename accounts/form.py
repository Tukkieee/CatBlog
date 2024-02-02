from django import forms
from .models import UserAccount 
from django.contrib.auth import password_validation
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class CusAuth(AuthenticationForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )
    class Meta:
        model = UserAccount
        fields = "__all__"
        

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )
    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'profile_image']
        # fields = ['title', 'body', 'date_published', 'publish']/
        widgets = {
            'first_name': forms.TextInput(attrs={ 'class':'form-control'}),
            'last_name': forms.TextInput(attrs={ 'class':'form-control'}),
            'username': forms.TextInput(attrs={ 'class':'form-control'}),
            'email': forms.EmailInput(attrs={ 'class':'form-control'}),
            'profile_image': forms.FileInput(attrs={ 'class':'form-control'}),
            
        }
        required_fields = ['first_name', 'last_name']


class UpdateUserForm(UserChangeForm):
    
    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_image']
        # fields = ['title', 'body', 'date_published', 'publish']/
        widgets = {
            'first_name': forms.TextInput(attrs={ 'class':'form-control'}),
            'last_name': forms.TextInput(attrs={ 'class':'form-control'}),
            'username': forms.TextInput(attrs={ 'class':'form-control'}),
            'email': forms.EmailInput(attrs={ 'class':'form-control'}),
            'profile_image': forms.FileInput(attrs={ 'class':'form-control'}),
            
        }
       