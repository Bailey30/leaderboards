from django import forms
from django.contrib.auth.forms import BaseUserCreationForm, AuthenticationForm


class ScoreForm(forms.Form):
    username = forms.CharField(label="Enter name", max_length=3)
    score = forms.IntegerField(label="Score")


class RegistrationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)


class LoginForm(AuthenticationForm):
    pass


class LogoutForm(forms.Form):
    pass
