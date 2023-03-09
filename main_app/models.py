from django.db import models
from django.urls import reverse
# bring in a copy of the User table so we can customize users to pur needs
from django.contrib.auth.models import AbstractUser, BaseUserManager

# custom user model overrides
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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        
class FanManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role = User.Role.FAN)


class FanUser(User):

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


class BandUser(User):

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


class VenueUser(User):

    base_role = User.Role.VENUE

    venue = VenueManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for venues."
    
# Other models
class Fan(models.model):
    display_name = models.CharField(max_length=25)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse("fan_detail", kwargs={"pk": self.pk})
    

class Band(models.Model):
    name = models.CharField(max_length=50)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.CharField(max_length=50)
    # hopefully tags can be implemented
    genre = models.CharField(max_length=50)
    user = models.ForeignKey(BandUser, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("band_detail", kwargs={"pk": self.pk})
    

class Venue(models.Model):
    name = models.CharField(max_length=50)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.CharField(max_length=50)
    # hopefully tags can be implemented
    genre = models.CharField(max_length=50)
    user = models.ForeignKey(VenueUser, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("venue_detail", kwargs={"pk": self.pk})
    

class Event(models.Model):
    start_date_time = models.DateTimeField('start date & time')
    end_date_time = models.DateTimeField('end date & time')
    ticket_price = models.DecimalField(decimal_places=2)
    note = models.TextField(max_length=250)
    # MtM field for bands
    bands = models.ManyToManyField(Band)
    # FK references
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("events_detail", kwargs={"event_id": self.id})
    

class Star(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)

# hmmm
# how do I access the id of either the venue or the band , depending on the heart
class Heart(models.Model):
    target = models.ForeignKey(Event, on_delete=models.CASCADE)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)