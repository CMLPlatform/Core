from django.conf.urls import url
import books.views as views

urlpatterns = [

       # url(r'^$', views.ExioVisuals, name='ExioVisuals'),
        url(r'^$', views.book_list, name='book_list'),
        url(r'^create/$', views.book_create, name='book_create'),
        url(r'^books/(?P<pk>\d+)/update/$', views.book_update, name='book_update'),
        url(r'^books/(?P<pk>\d+)/delete/$', views.book_delete, name='book_delete'),



]
