# admin.py
from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from PUMA.models import WeatherStation, Area, Lines, Comment


admin.site.register(WeatherStation, LeafletGeoAdmin)
admin.site.register(Area, LeafletGeoAdmin)
admin.site.register(Lines, LeafletGeoAdmin)
admin.site.register(Comment)