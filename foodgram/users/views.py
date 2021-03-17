from django.shortcuts import render 
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy 
 
from .forms import CreationForm, AuthForm, PassChangeForm, PassResetForm
 
 
class SignUp(CreateView):
    form_class = CreationForm 
    success_url = reverse_lazy('login') 
    template_name = 'registration/reg.html' 

class UserLoginView(LoginView):
    authentication_form = AuthForm

class PassChange(PasswordChangeView, LoginRequiredMixin):
    form_class = PassChangeForm

class PassReset(PasswordResetView):
    form_class = PassResetForm

