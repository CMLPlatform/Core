from django import forms

from PUMA.models import UserProfile
from django.contrib.auth.models import User
from leaflet.forms.widgets import LeafletWidget
from PUMA.models import WeatherStation, Area, Lines, Comment

class WeatherStationForm(forms.ModelForm):

    class Meta:
        model = WeatherStation
        fields = ('name', 'geom')
        widgets = {'geom': LeafletWidget()}


class AreaForm(forms.ModelForm):

    class Meta:
        model = Area
        fields = ('name', 'geom')
        widgets = {'geom': LeafletWidget()}


class LineForm(forms.ModelForm):

    class Meta:
        model = Lines
        fields = ('name', 'geom')
        widgets = {'geom': LeafletWidget()}


#THIS FORM CLASS CAN BE USED AS a registry template to register to the web appliction (NOT USED AS OF NOW)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text','email', 'affiliation', 'category', 'product')