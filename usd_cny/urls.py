# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from usd_cny.apps.transfer import views
from django.contrib import admin
import settings
admin.autodiscover()



urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'usd_cny.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^transfer/', include('usd_cny.apps.transfer.urls')),
                       url(r'^$', views.index, name='index'),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.STATIC_ROOT}),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),
                       )
