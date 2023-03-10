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
        instance.groups.set([group], clear=True)

# class FanManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role = User.Role.FAN)

#     base_role = User.Role.FAN

#     fan = FanManager()
#     class Meta:
#         proxy = True

#     def welcome(self):
#         return "Only for fans."


        
    

# class BandManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role = User.Role.BAND)


# class BandUser(User):

#     base_role = User.Role.BAND

#     band = BandManager()
#     class Meta:
#         proxy = True

#     def welcome(self):
#         return "Only for bands."
    
# class VenueManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role = User.Role.VENUE)


# class VenueUser(User):

#     base_role = User.Role.VENUE

#     venue = VenueManager()
#     class Meta:
#         proxy = True

#     def welcome(self):
#         return "Only for venues."
    
# # Other models

    
# class UserAccountManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError("Email field is required !")
#         if not username:
#             raise ValueError("Username field is required !")
#         if not password:
#             raise ValueError("Password field is required !")
#         user = self.model(
#             email=email,
#             username=username
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
 
#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             email=email, username=username, password=password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.is_admin = True
#         user.save()
#         return user
 
#     def create_fan(self, email, username, password):
#         user = self.create_user(email, username, password)
#         user.is_student = True
#         user.save()
#         return user
 
#     def create_venue(self, email, username, password):
#         user = self.create_user(email, username, password)
#         user.is_teacher = True
#         user.save()
#         return user
 
#     def create_band(self, email, username, password):
#         user = self.create_user(email, username, password)
#         user.is_principal = True
#         user.save()
#         return user
 
 
# class UserAccount(AbstractBaseUser):
#     username = models.CharField(max_length=200, blank=False, null=False)
#     email = models.CharField(
#         max_length=200, blank=False, null=False, unique=True)
 
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
 
#     is_fan = models.BooleanField(default=False)
#     is_venue = models.BooleanField(default=False)
#     is_band = models.BooleanField(default=False)
 
#     objects = UserAccountManager()
 
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ['username']
 
#     def __unicode__(self):
#         return str(self.username)
 
#     def has_perm(self, perm, obj=None):
#         return self.is_admin
 
#     def has_module_perms(self, app_label):
#         return True
    
class FanProfile(models.Model):
    display_name = models.CharField(max_length=25)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse("fan_detail", kwargs={"pk": self.pk})
    

class BandProfile(models.Model):
    name = models.CharField(max_length=50)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.CharField(max_length=50)
    # hopefully tags can be implemented
    genre = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("band_detail", kwargs={"pk": self.pk})
    

class VenueProfile(models.Model):
    name = models.CharField(max_length=50)
    # location should probably be it's own model, OtO 
    location = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.CharField(max_length=50)
    # hopefully tags can be implemented
    genre = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("venue_detail", kwargs={"pk": self.pk})
    
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