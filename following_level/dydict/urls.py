from django.conf.urls import patterns, url

from dydict.views import AboutView, HelpView


urlpatterns = patterns('dydict.views',
    url(r'^show_words/(?P<page_number>\d{1})/$', 'listWords'),
    url(r'^createuser/$', 'createUser'),
    url(r'^login/$', 'user_login'),
    url(r'^logout/$', 'user_logout'),
    url(r'^about/$', AboutView.as_view(), name="dydict_about"),
    url(r'^help/$', HelpView.as_view(), name="dydict_help"),
)
