from django.shortcuts import render, redirect
# GENERIC CLASS BASED VIEWS
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
# MODELS
from .models import Event, FanProfile, BandProfile, VenueProfile
# CUSTOM FORMS
from .forms import CustomUserCreationForm
# AUTH
from django.contrib.auth import login
# MIXINS
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# !! CHECK OUT PermissionsRequiredMixin
# to give routes permissions based on user role/group
# use with class-based views
class Home(TemplateView):
    template_name = "home.html"

#  VENUE PROFILE VIEWS
class VenueProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = BandProfile
    template_name = 'venue-details/details.html'

class VenueProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BandProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class VenueProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BandProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class VenueProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BandProfile
    success_url = '/venue-details/'  

#  BAND PROFILE VIEWS
class BandProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = BandProfile
    template_name = 'band-details/details.html'

class BandProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BandProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class BandProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BandProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class BandProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BandProfile
    success_url = '/band-details/'   

#  FAN PROFILE VIEWS
class FanProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = FanProfile
    template_name = 'fan-details/details.html'

class FanProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = FanProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class FanProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FanProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class FanProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = FanProfile
    success_url = '/fan-details/'

# EVENTS VIEWS
class EventList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    template_name = 'events/index.html'

class EventDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    template_name = 'events/details.html'

class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    fields = ['location', 'website', 'description', 'image', 'genre']

class EventUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    fields = ['location', 'website', 'description', 'image', 'genre']

class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'

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

