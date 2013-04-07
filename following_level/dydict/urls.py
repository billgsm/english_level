from django.conf.urls import patterns, url

urlpatterns = patterns('dydict.views',
    url(r'^show_words/$', 'listWords'),
    url(r'^createuser/$', 'createUser'),
    url(r'^login/$', 'login'),
)
