from django.conf.urls import  url
import PUMA.views as views

urlpatterns = [
       # url(r'^$', views.ExioVisuals, name='ExioVisuals'),
        url(r'^map/$', views.test, name='mapAmsterdam'),
        url(r'^transport/$', views.transport, name='mapAmsterdam'),
        url(r'^infrastructure/$', views.infrastructure, name='mapAmsterdam'),
        url(r'^commercial/$', views.commercial, name='mapAmsterdam'),
        url(r'^industrial/$', views.industrial, name='mapAmsterdam'),
        url(r'^public/$', views.public, name='mapAmsterdam'),
        url(r'^appliances/$', views.appliances, name='mapAmsterdam'),
        url(r'^oost/$', views.oost, name='mapAmsterdam'),
        url(r'^$', views.home, name='home'),
        url(r'^map/mapinfo$', views.info, name='info'),
         url(r'^register/$', views.user_login, name='EIOplot'),
        url(r'^logout/$', views.user_logout, name='EIOplot'),
        url(r'^post/$', views.add_comment_to_post, name='add_comment_to_post'),
]
