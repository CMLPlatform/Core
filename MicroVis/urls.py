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
        url(r'^sandd/$', views.sandd, name='softwaredata'),
        url(r'^sandd2/$', views.sandd2, name='softwaredata'),
        url(r'^sandd3/$', views.sandd3, name='softwaredata'),
        url(r'^sandd4/$', views.sandd4, name='softwaredata'),
        url(r'^sandd5/$', views.sandd5, name='softwaredata'),
        url(r'^sandd6/$', views.sandd6, name='softwaredata'),
        url(r'^sandd7/$', views.sandd7, name='softwaredata'),
        url(r'^sandd8/$', views.sandd8, name='softwaredata'),
        url(r'^sandd9/$', views.sandd9, name='softwaredata'),

]
