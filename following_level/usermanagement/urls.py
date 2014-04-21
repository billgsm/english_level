# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.views import (password_reset, password_reset_done,
        password_reset_complete, password_reset_confirm)
from django.contrib.auth.decorators import login_required

from usermanagement.views import editProfile


urlpatterns = patterns('usermanagement.views',
    url(r'^createuser/$', 'createUser', name="create_account"),
    url(r'^login/?$', 'user_login', name='login'),
    url(r'^logout/?$', 'user_logout', name='logout'),
    url(r'^edit_profile/?$', login_required(editProfile), name='edit_profile'),
    ################
    # Reset password
    ################
    url(r'^password/reinit/$', password_reset,
            {
                'post_reset_redirect': '/user/password/reset/done/',
                'template_name': 'usermanagement/password_reset_form.html'
            },
            name='password_reset'
       ),
    url(r'^password/reset/done/$', password_reset_done,
            {'template_name': 'usermanagement/password_reset_done.html'},
       ),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/done/$',
            password_reset_confirm,
            {
                'post_reset_redirect': '/user/password/done/',
                'template_name': 'usermanagement/password_reset_confirm.html'
            }
        ),
    url(r'^password/done/$', password_reset_complete,
            {
                'template_name': 'usermanagement/password_reset_complete.html'
            }
       ),
)
