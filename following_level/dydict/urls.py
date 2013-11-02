from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from dydict.views import AboutView, HelpView, Word_List, CreateDict
from dydict.models import Dict
from dydict.forms import WordForm


urlpatterns = patterns('dydict.views',
    # Generic views
    url(r'^list/?$', login_required(Word_List.as_view()), name="list"),
    url(r'^(?P<pk>\d+)/details/?$', DetailView.as_view(model=Dict), name="details"),
    url(r'^(?P<pk>\d+)/update/$', UpdateView.as_view(model=Dict,
      form_class=WordForm), name='update'),
    url(r'^create/$', CreateDict.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/delete/$', DeleteView.as_view(
      model=Dict, success_url=reverse_lazy('list')), name='delete'),

    #url(r'^show_words/?$', 'listWords'),
    #url(r'^show_words/(?P<page_number>\d{1})/?$', 'listWords'),
    url(r'^createuser/$', 'createUser', name="create_account"),
    url(r'^login/$', 'user_login', name='login'),
    url(r'^logout/$', 'user_logout', name='logout'),
    url(r'^about/$', AboutView.as_view(), name="dydict_about"),
    url(r'^help/$', HelpView.as_view(), name="dydict_help"),
)
