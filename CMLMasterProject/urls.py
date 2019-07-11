"""CMLMasterProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import CMLMasterProject.views as views
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import views as auth_views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$', views.homePage, name='homePage'),
    url(r'^login/$', auth_views.LoginView,{'template_name': 'CMLMasterProject/login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^exploratory/', views.exploratory, name='exploratory'),
    # url(r'^', include('snippets.urls')),
    # url(r'^', include('ramascene.urls')),
    url(r'^about/', views.about, name='about'),
    url(r'^puma/', include('PUMA.urls')),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
url(r'^research/microvis/', include('MicroVis.urls')),
    url(r'^sign-up/$', views.signup, name='signup'),
    url(r'^cml-sign-up/$', views.cml_signup, name='signup'),
    url(r'^cms-admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    # url(r'^research/', include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)