from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from guess_meaning.views import createGuessMeaning


urlpatterns = patterns('guess_meaning.views',
    url(r'^guess/$', login_required(createGuessMeaning),
        name='guess'),
)
