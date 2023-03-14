from django.db import models, transaction

from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
# bring in a copy of the User table so we can customize users to pur needs
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group

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
def user(sender: CustomUser, instance: CustomUser, created, ** kwargs) -> None:
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
        return reverse("fans_detail", kwargs={"fan_id": self.id})
    
    def __str__(self):
        if self.display_name:
            return self.display_name
        else:
            return str(self.user_id)
    
@receiver(post_save, sender=CustomUser)
def create_fan_profile(sender, instance, created, **kwargs):
    if instance.role == 1 and created:
        FanProfile.objects.create(user=instance)

class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Mood(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class BandProfile(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.CharField(max_length=50, null=True, blank=True)
    # hopefully tags can be implemented
    # genre = models.CharField(max_length=1, choices=GENRES, null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    # mood = models.CharField(max_length=1, choices=MOODS, null=True, blank=True)
    moods = models.ManyToManyField(Mood)
    # link a profile to a user
    # i think i want one user to have only one profile (for now)
    # so maybe use a OtO relation instead?
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        permissions = (
            ("dashboard", "access band dashboard"),
       )
        
    def get_absolute_url(self):
        return reverse("bands_detail", kwargs={"band_id": self.id})
    
    def __str__(self):
        return self.name
    
@receiver(post_save, sender=CustomUser)
def create_band_profile(sender, instance, created, **kwargs):
    if instance.role == 2 and created:
        BandProfile.objects.create(user=instance)

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
        return reverse("venues_detail", kwargs={"venue_id": venue_id})
    
    def __str__(self):
        return self.name
    
@receiver(post_save, sender=CustomUser)
def create_venue_profile(sender, instance, created, **kwargs):
    if instance.role == 3 and created:
        VenueProfile.objects.create(user=instance)
    
class Event(models.Model):
    date = models.DateField('date', null=True, blank=True)
    time = models.CharField(max_length=20, null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=7, decimal_places=2)
    note = models.TextField(max_length=250)
    # MtM field for bands
    bands = models.ManyToManyField(BandProfile)
    venue = models.ForeignKey(VenueProfile, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('events_detail', kwargs={'event_id': self.id})
    

class Star(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fan = models.ForeignKey(FanProfile, on_delete=models.CASCADE)

# hmmm
# how do I access the id of either the venue or the band , depending on the heart
class Heart(models.Model):
    target = models.ForeignKey(Event, on_delete=models.CASCADE)
    fan = models.ForeignKey(FanProfile, on_delete=models.CASCADE)