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
class VenueList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = VenueProfile
    template_name = 'venues/index.html'
class VenueProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = VenueProfile
    template_name = 'venues/details.html'

class VenueProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = VenueProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class VenueProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = VenueProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class VenueProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = VenueProfile
    success_url = '/venues/'  

#  BAND PROFILE VIEWS
class BandList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BandProfile
    template_name = 'bands/index.html'
class BandProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = BandProfile
    template_name = 'bands/details.html'

class BandProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BandProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class BandProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BandProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class BandProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BandProfile
    success_url = '/bands/'   

#  FAN PROFILE VIEWS
class FanList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = FanProfile
    template_name = 'fans/index.html'
class FanProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = FanProfile
    template_name = 'fans/details.html'

class FanProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = FanProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class FanProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FanProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class FanProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = FanProfile
    success_url = '/fans/'

# EVENTS VIEWS
class EventList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    template_name = 'events/index.html'

class EventDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Event
    template_name = 'events/details.html'

class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    fields = ['location', 'website', 'description', 'image', 'genre', 'mood']

class EventUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    fields = ['location', 'website', 'description', 'image', 'genre', 'mood']

class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data('role')
            user = form.save()
            login(request, user)
            return redirect(f'{role}s/create')
        else:
            error_message  = 'Invalid sign up - please try again.'
    form = CustomUserCreationForm()
    context = {'form': form, 'error_massage': error_message}
    return render(request, 'registration/signup.html', context)

