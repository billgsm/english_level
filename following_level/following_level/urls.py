# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^dictionary/', include('dydict.urls')),
    url(r'^user/', include('usermanagement.urls')),
    url(r'^test/', include('guess_meaning.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^.*$', 'usermanagement.views.user_login'),
    #url(r'^.*$', RedirectView.as_view(url='/user/login', permanent=False),
    #    name='index'),
)
