from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from models import BBSitting

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^login$', auth_views.login, name="login"),
    url(r'^agenda$', ListView.as_view(model=BBSitting)),
    url(r'^get/(?P<pk>\d+)$', DetailView.as_view(model=BBSitting), name="detail"),
    url(r'^new$', CreateView.as_view(model=BBSitting)),
    url(r'^admin/', include(admin.site.urls)),
)
