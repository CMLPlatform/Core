from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    authentication_key = forms.CharField(widget=forms.PasswordInput(),max_length=254, required=True, help_text='Required. Credentials are given by CML moderators of the platform.')
    topics = forms.CharField(max_length=254, required=True, help_text='Required. Please separate research topics by commas.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(label="Password", required=True, help_text="1) Your password can't be too similar to your other personal information. 2) Your password must contain at least 8 characters. 3) Your password can't be a commonly used password. 4) Your password can't be entirely numeric.", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'authentication_key', 'topics', 'email', 'password1', 'password2', )

