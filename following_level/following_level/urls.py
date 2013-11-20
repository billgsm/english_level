# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'following_level.views.home', name='home'),
    url(r'^dictionary/', include('dydict.urls')),
    url(r'^user/', include('usermanagement.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
