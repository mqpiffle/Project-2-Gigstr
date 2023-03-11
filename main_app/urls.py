from django.urls import path
from . import views 
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    # PROFILE URLS
    # FANS
    path('fans/', views.FanList.as_view(), name='fans_index'),
    path('fans/<int:pk>/', views.FanProfileDetail.as_view(), name='fans_profile_detail'),
    path('fans/create/', views.FanProfileCreate.as_view(), name='fans_profile_create'),
    path('fans/<int:pk>/update/', views.FanProfileUpdate.as_view(), name='fans_profile_update'),
    path('fans/<int:pk>/delete/', views.FanProfileDelete.as_view(), name='fans_profile_delete'),
    # BANDS
    path('bands/', views.BandList.as_view(), name='bands_index'),
    path('bands/<int:pk>/', views.BandProfileDetail.as_view(), name='bands_profile_detail'),
    path('bands/create/', views.BandProfileCreate.as_view(), name='bands_profile_create'),
    path('bands/<int:pk>/update/', views.BandProfileUpdate.as_view(), name='bands_profile_update'),
    path('bands/<int:pk>/delete/', views.BandProfileDelete.as_view(), name='bands_profile_delete'),
    # VENUES
    path('venues/', views.VenueList.as_view(), name='venues_index'),
    path('venues/<int:pk>/', views.VenueProfileDetail.as_view(), name='venues_profile_detail'),
    path('venues/create/', views.VenueProfileCreate.as_view(), name='venues_profile_create'),
    path('venues/<int:pk>/update/', views.VenueProfileUpdate.as_view(), name='venues_profile_update'),
    path('venues/<int:pk>/delete/', views.VenueProfileDelete.as_view(), name='venues_profile_delete'),
    # EVENTS URLS
    path('events/', views.EventList.as_view(), name='events_index'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='events_detail'),
    path('events/create/', views.EventCreate.as_view(), name='events_profile_create'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_profile_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_profile_delete'),
]
