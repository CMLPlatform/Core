from django.conf.urls import url
from django.urls import path
import circumat.views as views

urlpatterns = [
    url(r'^$', views.home_page, name='home-page'),
    url(r'^edu/$', views.edu_page, name='educational-materials'),
    url(r'^online-tools/$', views.online_tools, name='onlineTools'),
    url(r'^online-databases/$', views.online_databases, name='onlineDatabases'),
    url(r'^project-summary/$', views.project_summary, name='projectSummary'),
    url(r'^circular-economy/$', views.circular_economy, name='circularEconomy'),
    url(r'^academic-papers/$', views.academic_papers, name='academicPapers'),
    path('circumat/', views.home, name='home'),
    path('ajaxhandling/', views.ajaxHandling, name='ajaxhandling'),

]
