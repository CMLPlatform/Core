from django.conf.urls import  url
import panorama.views as views
urlpatterns = [
        url(r'^$', views.home, name='panorama_home'),
        url(r'^services/$', views.services, name='panorama_services'),
        url(r'^about/$', views.about, name='panorama_about'),
        url(r'^contact/$', views.contact, name='panorama_contact'),
]