from django import forms 
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user