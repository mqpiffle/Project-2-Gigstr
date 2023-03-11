from django.db import models, transaction

from django.urls import reverse
from django.db.models.signals import post_save
# bring in a copy of the User table so we can customize users to pur needs
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
# custom user model overrides
class CustomUser(AbstractUser):
    # define a set of choices for the role field
    # describing the types of user for the app
    # this will lead to the user types having permissions
    # to access certain parts of the app
    class Roles(models.IntegerChoices):
        ADMIN = 0, _('Admin')
        FAN = 1, _('Fan')
        BAND = 2, _('Band')
        VENUE = 3, _('Venue')

    # add the role field
    role = models.IntegerField(choices=Roles.choices, default=Roles.FAN, verbose_name=_('Role'))
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.role = self.base_role
    #         return super().save(*args, **kwargs)
        
GROUPS = ['Admin', 'Fan', 'Band', 'Venue']
@receiver(post_save, sender=CustomUser)
def user(sender: CustomUser, instance: CustomUser, ** kwargs) -> None:
        group = Group.objects.get(name=GROUPS[instance.role])
        transaction.on_commit(lambda: instance.groups.set([group], clear=True))

# USER PROFILES
# on base account sign up, user will be redirected
# to create a profile before continuing   
class FanProfile(models.Model):
    display_name = models.CharField(max_length=25, null=True, blank=True)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("fan_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.display_name
    
class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Mood(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class BandProfile(models.Model):
    # GENRES = (
    #     ('J', _('Jazz')),
    #     ('B', _('Blues')),
    #     ('R', _('Rock')),
    #     ('M', _('Metal')),
    #     ('P', _('Punk')),
    #     ('K', _('Funk')),
    #     ('Z', _('Pop')),
    #     ('C', _('Classical')),
    #     ('F', _('Folk')),
    #     ('W', _('World')),
    #     ('D', _('Dance')),
    #     ('E', _('Electronic')),
    #     ('A', _('Acoustic')),
    #     ('Y', _('Yacht Rock')),
    #     ('X', _('Covers')),
    #     ('O', _('Originals')),
    # )

    # MOODS = (
    #     ('A', _('Aggressive')),
    #     ('L', _('Lively')),
    #     ('E', _('Energetic')),
    #     ('L', _('Loud')),
    #     ('D', _('Dynamic')),
    # )

    name = models.CharField(max_length=50, null=True, blank=True)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=50, null=True, blank=True)
    # hopefully tags can be implemented
    # genre = models.CharField(max_length=1, choices=GENRES, null=True, blank=True)
    genres = models.ManyToManyField(Genre, null=True, blank=True)
    # mood = models.CharField(max_length=1, choices=MOODS, null=True, blank=True)
    moods = models.ManyToManyField(Mood, null=True, blank=True)
    # link a profile to a user
    # i think i want one user to have only one profile (for now)
    # so maybe use a OtO relation instead?
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("band_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.display_name

class VenueProfile(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=50, null=True, blank=True)
    # hopefully tags can be implemented
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("venue_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.display_name
    
class Event(models.Model):
    start_date_time = models.DateTimeField('start date & time')
    end_date_time = models.DateTimeField('end date & time')
    ticket_price = models.DecimalField(max_digits=7, decimal_places=2)
    note = models.TextField(max_length=250)
    # MtM field for bands
    bands = models.ManyToManyField(BandProfile)
    venue = models.ForeignKey(VenueProfile, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("events_detail", kwargs={"event_id": self.id})
    

class Star(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fan = models.ForeignKey(FanProfile, on_delete=models.CASCADE)

# hmmm
# how do I access the id of either the venue or the band , depending on the heart
class Heart(models.Model):
    target = models.ForeignKey(Event, on_delete=models.CASCADE)
    fan = models.ForeignKey(FanProfile, on_delete=models.CASCADE)