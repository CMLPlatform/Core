from django.conf.urls import url
from django.urls import path
import circumat.views as views

urlpatterns = [
    url(r'^$', views.home_page, name='home-page'),
    url(r'^online-tools/$', views.online_tools, name='onlineTools'),
    url(r'^online-databases/$', views.online_databases, name='onlineDatabases'),
    path('circumat/', views.home, name='home'),
    path('ajaxhandling/', views.ajaxHandling, name='ajaxhandling'),

]
