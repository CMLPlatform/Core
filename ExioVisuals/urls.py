from django.conf.urls import url
import ExioVisuals.views as views

urlpatterns = [
       # url(r'^$', views.ExioVisuals, name='ExioVisuals'),
        url(r'^$', views.home, name='home'),
        url(r'^distribution/$', views.distributionView, name='distribution'),
        url(r'^treemap/$', views.treemap, name='treemap'),
        url(r'^redirect/$', views.redirectView, name='redirect'),
        url(r'^geo/$', views.geo, name='geo'),
        url(r'^timeseries/$', views.timeseries, name='timeseries'),
        url(r'^supplychain/$', views.supplychain, name='supplychain'),
        url(r'^bla/$', views.test, name='test'),
        url(r'^ajax/$', views.ajax, name='Ajaxtest'),
        url(r'^infobutton/$', views.info, name='Ajaxtest'),



]
