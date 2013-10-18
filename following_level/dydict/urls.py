from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required

from dydict.views import AboutView, HelpView, Word_List
from dydict.models import Dict


urlpatterns = patterns('dydict.views',
    url(r'^show_words/?$', 'listWords'),
    url(r'^(?P<pk>\d+)/details/?$', DetailView.as_view(model=Dict), name="details"),
    url(r'^list/?$', login_required(Word_List.as_view()), name="list"),
    url(r'^show_words/(?P<page_number>\d{1})/?$', 'listWords'),
    url(r'^createuser/$', 'createUser'),
    url(r'^login/$', 'user_login'),
    url(r'^logout/$', 'user_logout'),
    url(r'^about/$', AboutView.as_view(), name="dydict_about"),
    url(r'^help/$', HelpView.as_view(), name="dydict_help"),
)
