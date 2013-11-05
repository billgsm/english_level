# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('usermanagement.views',
    url(r'^createuser/$', 'createUser', name="create_account"),
    url(r'^login/$', 'user_login', name='login'),
    url(r'^logout/$', 'user_logout', name='logout'),
)
