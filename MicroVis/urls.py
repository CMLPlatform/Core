from django.conf.urls import  url
import MicroVis.views as views

urlpatterns = [
       # url(r'^$', views.ExioVisuals, name='ExioVisuals'),
        url(r'^$', views.home, name='microvis'),
        url(r'^us-stocks/', views.us_stocks, name='us-stock'),
        url(r'^us-flows/', views.us_flows, name='use-flows'),
        url(r'^fishman/', views.flows_fishman, name='flows_fishman'),
        url(r'^tailing/', views.tailing, name='tailing'),

]
