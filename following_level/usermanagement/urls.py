# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.views import (password_reset, password_reset_done,
        password_reset_complete, password_reset_confirm)


urlpatterns = patterns('usermanagement.views',
    url(r'^createuser/$', 'createUser', name="create_account"),
    url(r'^login/$', 'user_login', name='login'),
    url(r'^logout/$', 'user_logout', name='logout'),
    ################
    # Reset password
    ################
    url(r'^password/reinit/$', password_reset,
        {'post_reset_redirect': '/user/password/reset/done/'},
        name='password_reset'),
    url(r'^password/reset/done/$', password_reset_done),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/done/$',
        password_reset_confirm, {'post_reset_redirect': '/user/password/done/'}),
    url(r'^password/done/$', password_reset_complete),
)
