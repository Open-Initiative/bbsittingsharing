from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from models import BBSitting, Parent
from views import SearchView

from django.contrib import admin
admin.autodiscover()

parentFields = ['first_name', 'last_name', 'email', 'phone', 'kidsnb', 'school', 'bbsitter', 'ok_at_home', 'ok_at_others']

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^info$', TemplateView.as_view(template_name="info.html"), name="info"),
    url(r'^search/(?P<date>\d+)$', SearchView.as_view(), name="search"),
    url(r'^agenda$', ListView.as_view(model=BBSitting), name="agenda"),
    url(r'^get/(?P<pk>\d+)$', DetailView.as_view(model=BBSitting), name="detail"),
    url(r'^book/(?P<pk>\d+)$', TemplateView.as_view(template_name="bbsittingsharing/book_confirm.html"), name="book"),
    url(r'^new$', CreateView.as_view(model=BBSitting), name="new"),
    url(r'^users/(?P<slug>\w+)/$', DetailView.as_view(model=Parent, slug_field='username'), name="profile"),
    url(r'^users/(?P<slug>\w+)/edit$', UpdateView.as_view(model=Parent, slug_field='username', fields=parentFields), name="profile_edit"),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
