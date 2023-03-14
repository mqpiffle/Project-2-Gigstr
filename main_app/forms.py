from django.forms import ModelForm
from .models import CustomUser, Event
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    # def save(self, commit=True):
    #     user = super(CustomUserCreationForm, self).save(commit=False)
    #     user.role = self.cleaned_data['role']
    #     if commit:
    #         user.save()
    #     return user
    
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'time', 'ticket_price', 'note', 'bands', 'venue']