from django.shortcuts import render, redirect
# GENERIC CLASS BASED VIEWS
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
# MODELS
from .models import Event, FanProfile, BandProfile, VenueProfile
# CUSTOM FORMS
from .forms import CustomUserCreationForm, EventForm
# AUTH
from django.contrib.auth import login, authenticate
# MIXINS AND DECORATORS
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
# PYTHON DEBUGGING TOOL
import pdb
# !! CHECK OUT PermissionsRequiredMixin
# to give routes permissions based on user role/group
# use with class-based views
# class Home(TemplateView):
#     template_name = "home.html"

# function view
# first step is to recreate the home view on its own with a custom view
def home(request):
    # pdb.set_trace()
# next step - see if the home view can process their role
    if request.user.is_authenticated:
        user = request.user
        role = user.role
        print(user.id)
        #     # next see if 'if else' redirects from the login view 
        # if user is not None:
            # user = authenticate(username=username, password=password)
        if user.is_active:
            if role == 1:
                fan_profile = FanProfile.objects.get(user=user.id)
                return redirect('gigstr:fans_detail', fan_id=fan_profile.id)
            if role == 2:
                band_profile = BandProfile.objects.get(user=user.id)
                return redirect('gigstr:bands_detail', band_id=band_profile.id)
            if role == 3:
                venue_profile = VenueProfile.objects.get(user=user.id)
                return redirect('gigstr:venues_detail', venue_id=venue_profile.id)
                
    return render(request, 'home.html')


#  VENUE PROFILE VIEWS
class VenueList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'main_app.view_venueprofile'
    model = VenueProfile
    template_name = 'venues/index.html'
# class VenueProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
#     permission_required = 'main_app.view_venueprofile'
#     model = VenueProfile
#     template_name = 'venues/details.html'
@login_required
@permission_required('main_app.view_venueprofile')
def VenueProfileDetail(request, venue_id):
    venue = VenueProfile.objects.get(user=request.user.id)
    venue_events = Event.objects.filter(venue=venue_id)
    return render(request, 'venues/details.html', {'venue_profile': venue, 'venue_events': venue_events})

class VenueProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main_app.add_venueprofile'
    model = VenueProfile
    fields = ['name', 'location', 'website','description', 'image']

class VenueProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main_app.change_venueprofile'
    model = VenueProfile
    fields = ['name', 'location', 'website','description', 'image']

class VenueProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main_app.delete_venueprofile'
    model = VenueProfile
    success_url = '/venues/'  

#  BAND PROFILE VIEWS
class BandList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'main_app.view_bandprofile'
    model = BandProfile
    template_name = 'bands/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bands'] = BandProfile.objects.all()
        return context
# class BandProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
#     permission_required = 'main_app.view_bandprofile'
#     model = BandProfile
#     template_name = 'bands/details.html'

#     def get_context_data(self, **kwargs):
#         band = BandProfile.objects.get(id=self.kwargs['band_id'])
#         context = super().get_context_data(**kwargs)
#         context['our_events'] = Event.objects.filter(bands=band)
#         context['band_profile'] = band
#         return context
@login_required
@permission_required('main_app.view_bandprofile')
def BandProfileDetail(request, band_id):
    band = BandProfile.objects.get(user=request.user.id)
    band_events = Event.objects.filter(bands=band_id)
    return render(request, 'bands/details.html', {'band_profile': band, 'band_events': band_events})
    
class BandProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main_app.add_bandprofile'
    model = BandProfile
    fields = ['name', 'location', 'website','description', 'image', 'genres', 'moods']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    # trying to redirect if a user tries to access create route
    # when then is already a profile, can't get redirect to work
    # don't know how to access pk

    # def get(self, *args, **kwargs):
    #     if self.model.objects.get(user=self.request.user):
    #         return redirect('bands_profile_update')
    #     else:
    #         return super().get(*args, **kwargs)
        
class BandProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main_app.change_bandprofile'
    model = BandProfile
    fields = ['name', 'location', 'website','description', 'image', 'genres', 'moods']

class BandProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main_app.delete_bandprofile'
    model = BandProfile
    success_url = '/bands/'   

#  FAN PROFILE VIEWS
class FanList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'main_app.view_fanprofile'
    model = FanProfile
    template_name = 'fans/index.html'
# class FanProfileDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
#     permission_required = 'main_app.view_fanprofile'
#     model = FanProfile
#     template_name = 'fans/details.html'
@login_required
@permission_required('main_app.view_fanprofile')
def FanProfileDetail(request, fan_id):
    fan = FanProfile.objects.get(user=request.user.id)
    # band_events = Event.objects.filter(bands=band_id)
    return render(request, 'fans/details.html', {'fan_profile': fan})

class FanProfileCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main_app.add_fanprofile'
    model = FanProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class FanProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main_app.change_fanprofile'
    model = FanProfile
    fields = ['display_name', 'location', 'website','description', 'image']

class FanProfileDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main_app.delete_fanprofile'
    model = FanProfile
    success_url = '/fans/'

# EVENTS VIEWS
class EventList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'main_app.view_event'
    model = Event
    template_name = 'events/index.html'
    

# class EventDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
#     permission_required = 'main_app.view_event'
#     model = Event
#     template_name = 'events/details.html'
@login_required
@permission_required('main_app.view_event')
def EventDetail(request, event_id):
    event = Event.objects.get(id=event_id)
    bands_ids = event.bands.all().values_list('id')
    event_bands = BandProfile.objects.filter(id__in=bands_ids)
    # band = BandProfile.objects.get(user=request.user.id)
    # band_events = Event.objects.filter(bands=band_id)
    return render(request, 'events/details.html', {'event': event, 'event_bands': event_bands})

class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'main_app.add_event'
    form_class = EventForm
    model = Event

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    # def get_success_url(self):
    #     return '/'
    

class EventUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'main_app.change_event'
    model = Event
    fields = ['date', 'time', 'ticket_price', 'note', 'bands', 'venue']

class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'main_app.delete_event'
    model = Event
    success_url = 'gigstr:home'

# class Login(View):
#     def get(self, request):
#         return render(request, 'registration/login.html')

#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']

#         if request.user is not None:
#             user = authenticate(username=username, password=password)
#             if user.is_active:
#                 login(request, user)
#                 if user.role == 'Band':
#                     return redirect('gigstr:bands_details')
#                 if user.role == 'Venue':
#                     return redirect('gigstr:venue_details')
#                 if user.role == 'Fan':
#                     return redirect('gigstr:fan_details')
        
#         return render(request, 'registration/login.html')


def signup(request):
    # pdb.set_trace()
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('gigstr:home')
        else:
            error_message  = 'Invalid sign up - please try again.'
    form = CustomUserCreationForm()
    context = {'form': form, 'error_massage': error_message}
    return render(request, 'registration/signup.html', context)

