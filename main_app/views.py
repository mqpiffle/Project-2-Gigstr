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
    permission_required = 'main_app.view_venue_profile'
    model = VenueProfile
    template_name = 'venues/index.html'
class VenueProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'main_app.view_venue_profile'
    model = VenueProfile
    template_name = 'venues/details.html'

class VenueProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main_app.add_venue_profile'
    model = VenueProfile
    fields = ['name', 'location', 'website','description', 'image']

class VenueProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main_app.set_venue_profile'
    model = VenueProfile
    fields = ['name', 'location', 'website','description', 'image']

class VenueProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main_app.remove_venue_profile'
    model = VenueProfile
    success_url = '/venues/'  

#  BAND PROFILE VIEWS
class BandList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'main_app.view_band_profile'
    model = BandProfile
    template_name = 'bands/index.html'
class BandProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'main_app.view_band_profile'
    model = BandProfile
    template_name = 'bands/details.html'

class BandProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main_app.add_bandprofile'
    model = BandProfile
    fields = ['name', 'location', 'website','description', 'image', 'genres', 'moods']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.model.objects.get(user=self.request.user):
            return redirect('bands_profile_update', self.objects.pk.get())
        else:
            return super().get(*args, **kwargs)
        
class BandProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main_app.set_band_profile'
    model = BandProfile
    fields = ['name', 'location', 'website','description', 'image', 'genres', 'moods']

class BandProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main_app.remove_band_profile'
    model = BandProfile
    success_url = '/bands/'   

#  FAN PROFILE VIEWS
class FanList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'main_app.view_fan_profile'
    model = FanProfile
    template_name = 'fans/index.html'
class FanProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'main_app.view_fan_profile'
    model = FanProfile
    template_name = 'fans/details.html'

class FanProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main_app.add_fan_profile'
    model = FanProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class FanProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main_app.set_fan_profile'
    model = VenueProfile
    model = FanProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class FanProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main_app.remove_fan_profile'
    model = FanProfile
    success_url = '/fans/'

# EVENTS VIEWS
class EventList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'main_app.view_event'
    model = Event
    template_name = 'events/index.html'

class EventDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'main_app.view_event'
    model = Event
    template_name = 'events/details.html'

class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main_app.add_event'
    model = Event
    fields = ['start_date_time', 'end_date_time', 'ticket_price', 'note', 'bands', 'venue']

class EventUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main_app.set_event'
    model = VenueProfile
    model = Event
    fields = ['start_date_time', 'end_date_time', 'ticket_price', 'note', 'bands', 'venue']

class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main_app.remove_event'
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

