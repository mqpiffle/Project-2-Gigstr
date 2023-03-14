from django.urls import path
from . import views 
from django.contrib.auth.views import LoginView

app_name = 'gigstr' 

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('accounts/login/', views.login, name='login'),
    # PROFILE URLS
    # FANS
    path('fans/', views.FanList.as_view(), name='fans_index'),
    path('fans/<int:fan_id>/', views.FanProfileDetail.as_view(), name='fans_detail'),
    path('fans/create/', views.FanProfileCreate.as_view(), name='fans_create'),
    path('fans/<int:fan_id>/update/', views.FanProfileUpdate.as_view(), name='fans_update'),
    path('fans/<int:pk>/delete/', views.FanProfileDelete.as_view(), name='fans_delete'),
    # BANDS
    path('bands/', views.BandList.as_view(), name='bands_index'),
    path('bands/<int:band_id>/', views.BandProfileDetail, name='bands_detail'),
    path('bands/create/', views.BandProfileCreate.as_view(), name='bands_create'),
    path('bands/<int:pk>/update/', views.BandProfileUpdate.as_view(), name='bands_update'),
    path('bands/<int:pk>/delete/', views.BandProfileDelete.as_view(), name='bands_delete'),
    # path('bands/<int:event_id>/dashboard/', views.BandDashboard.as_view(), name='bands_dashboard'),
    # VENUES
    path('venues/', views.VenueList.as_view(), name='venues_index'),
    path('venues/<int:pk>/', views.VenueProfileDetail.as_view(), name='venues_detail'),
    path('venues/create/', views.VenueProfileCreate.as_view(), name='venues_create'),
    path('venues/<int:pk>/update/', views.VenueProfileUpdate.as_view(), name='venues_update'),
    path('venues/<int:pk>/delete/', views.VenueProfileDelete.as_view(), name='venues_delete'),
    # EVENTS URLS
    path('events/', views.EventList.as_view(), name='events_index'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='events_detail'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
]
