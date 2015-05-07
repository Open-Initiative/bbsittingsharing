from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.views import generic
from models import BBSitting, Parent
from views import SearchView, CreateView

from django.contrib import admin
admin.autodiscover()

parentFields = ['first_name', 'last_name', 'email', 'phone', 'kidsnb', 'school', 'bbsitter', 'ok_at_home', 'ok_at_others']

urlpatterns = patterns('',
    url(r'^$', generic.TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^info$', generic.TemplateView.as_view(template_name="info.html"), name="info"),
    url(r'^search/(?P<date>\d+)$', SearchView.as_view(), name="search"),
    url(r'^agenda$', generic.ListView.as_view(model=BBSitting), name="agenda"),
    url(r'^get/(?P<pk>\d+)$', generic.DetailView.as_view(model=BBSitting), name="detail"),
    url(r'^book/(?P<pk>\d+)$', generic.TemplateView.as_view(template_name="bbsittingsharing/book_confirm.html"), name="book"),
    url(r'^new$', CreateView.as_view(model=BBSitting), name="new"),
    url(r'^users/(?P<slug>\w+)/$', generic.DetailView.as_view(model=Parent, slug_field='username'), name="profile"),
    url(r'^users/(?P<slug>\w+)/edit$', generic.UpdateView.as_view(model=Parent, slug_field='username', fields=parentFields), name="profile_edit"),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
