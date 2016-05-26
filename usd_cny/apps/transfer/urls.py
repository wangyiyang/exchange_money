# urls.py

#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'^transfersubmit/$', views.transfersubmit, name='transfersubmit'),
                       url(r'^success/$', views.success, name='success'),
                       url(r'^transfer_exchange/$', views.transfer_exchange, name='transfer_exchange'),
                       url(r'^$', views.transfer, name='transfer'),
                       url(r'^login$', views.login, name='login'),
                       url(r'^get_all_platforms_balance', views.get_all_platforms_balance, name='get_all_platforms_balance'),
                       )
