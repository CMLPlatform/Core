from django.conf.urls import  url
import MicroVis.views as views

urlpatterns = [
       # url(r'^$', views.ExioVisuals, name='ExioVisuals'),
        url(r'^$', views.home, name='microvis'),

        url(r'^fishman/', views.flows_fishman, name='flows_fishman'),
        url(r'^fishman2/', views.flows_fishman2, name='flows_fishman2'),
        url(r'^tailing/', views.tailing, name='tailing'),
        url(r'^fishman-default/$', views.fishmanDefView.as_view()),
        url(r'^fishman-jp-abs/$', views.fishman_JP_abs.as_view()),
        url(r'^fishman-jp-cap/$', views.fishman_JP_cap.as_view()),
        url(r'^fishman-jp-gdp/$', views.fishman_JP_gdp.as_view()),
        url(r'^fishman-jp-growth/$', views.fishman_JP_growth.as_view()),
        url(r'^fishman-jp-percent/$', views.fishman_JP_percent.as_view()),
        url(r'^fishman-us-cap/$', views.fishman_US_cap.as_view()),
        url(r'^fishman-us-gdp/$', views.fishman_US_gdp.as_view()),
        url(r'^fishman-us-growth/$', views.fishman_US_growth.as_view()),
        url(r'^fishman-us-percent/$', views.fishman_US_percent.as_view()),
        url(r'^fishman-default2/$', views.fishmanDefView2.as_view()),

]
