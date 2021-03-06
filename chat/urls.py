from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('registration.urls')),
    url(r'^$', 'chat.views.index', name='index'),
    url(r'^chat/(.+)/$', 'chat.views.chat', name='chat'),
)
