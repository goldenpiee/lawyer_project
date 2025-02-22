from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'full_name', 
            'phone', 
            'password1', 
            'password2'
        ]
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

    class Meta:
        model = User
        fields = ['email', 'password']