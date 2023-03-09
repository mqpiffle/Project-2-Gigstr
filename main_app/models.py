from django.db import models
# bring in a copy of the User table so we can customize users to pur needs
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    # define a set of choices for the role field
    # describing the types of user for the app
    # this will lead to the user types having permissions
    # to access certain parts of the app
    class Role(models.TextChoices):
        ADMIN = 'Admin',
        FAN = 'Fan',
        BAND = 'Band',
        VENUE = 'Venue',
    
    # set the default role
    base_role = Role.ADMIN

    # add the role field
    role = models.CharField(max_length=10, choices=Role.choices)
    # add other custom fields for all users
    website = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        
class FanManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = User.Role.FAN)


class Fan(User):

    base_role = User.Role.FAN

    fan = FanManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for fans."
    

class BandManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = User.Role.BAND)


class Band(User):

    base_role = User.Role.BAND

    band = BandManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for bands."
    
class VenueManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = User.Role.VENUE)


class Venue(User):

    base_role = User.Role.VENUE

    venue = VenueManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for venues."