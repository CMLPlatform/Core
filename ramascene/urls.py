from django.conf.urls import  url
import ramascene.views as views

urlpatterns = [
       # url(r'^$', views.ExioVisuals, name='ExioVisuals'),
        url(r'^ramascene/$', views.home, name='home'),

]