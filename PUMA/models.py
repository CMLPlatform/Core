from djgeojson.fields import PointField
from django.db import models
from djgeojson.fields import PolygonField, LineStringField, MultiLineStringField

from django.utils import timezone
# models.py
from djgeojson.fields import PointField
from django.db import models
from django.contrib.auth.models import User



class WeatherStation(models.Model):
    name = models.TextField()

    geom = PointField()


    description = models.TextField()

    def __str__(self):
        return self.name

    picture = models.ImageField()
    @property
    def popupContent(self):
       return '<p>{}</p><img src="{}" />'.format(
          self.description,
          self.picture.url)




class Area(models.Model):
    name = models.TextField()
    geom = PolygonField()


    description = models.TextField()
    color = models.TextField()
    picture = models.ImageField()
    def __str__(self):
        return self.name

    @property
    def popupContent(self):
       return '<p>{}</p><img src="{}" />'.format(
          self.description,
          self.picture.url)

    @property
    def colors(self):
        return self.color



class Lines(models.Model):
    name = models.TextField()
    geom = MultiLineStringField()

    picture = models.ImageField()
    description = models.TextField()
    color = models.TextField()

    def __str__(self):
        return self.name

    @property
    def popupContent(self):
       return '<p>{}</p><img src="{}" />'.format(
          self.description,
          self.picture.url)

    @property
    def colors(self):
        return self.color



class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Comment(models.Model):
    author = models.CharField(max_length=200)
    text = models.TextField(max_length=240)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)
    email = models.EmailField(max_length=254,default='...@...')
    affiliation = models.CharField(max_length=200, default='')
    category =  models.CharField(max_length=200, default='')
    product =  models.CharField(max_length=200, default='')
    #add email address #afficilation # product # category
    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.author+" | "+ str(self.created_date)

