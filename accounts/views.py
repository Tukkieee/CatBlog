from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, CreateView, RedirectView
from .models import UserAccount
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm, CusAuth
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout


# Create your views here.
class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = "Registration successful. You can now log in."

class SignInView(LoginView):
    form_class= CusAuth
    template_name = 'registration/login.html'
    # success_url = reverse('/')

# class LogoutView(RedirectView):
    
#     next_page = reverse_lazy('home')