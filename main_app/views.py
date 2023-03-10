from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
# CUSTOM FORMS
from .forms import CustomUserCreationForm
# AUTH
from django.contrib.auth import login
from django.contrib.auth.forms import  UserCreationForm
# MIXINS
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# !! CHECK OUT PermissionsRequiredMixin
# to give routes permissions based on user role/group
# use with class-based views
class Home(TemplateView):
    template_name = "home.html"


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message  = 'Invalid sign up - please try again.'
    form = CustomUserCreationForm()
    context = {'form': form, 'error_massage': error_message}
    return render(request, 'registration/signup.html', context)

