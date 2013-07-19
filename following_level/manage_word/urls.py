from django.conf.urls import patterns, url

urlpatterns = patterns('manage_word.views',
    url(r'^remove_words/?$', 'removeWords'),
    url(r'^hide_words/?$', 'hideWords'),
    url(r'^edit_words/(?P<word>.+)/?$', 'editWords'),
    url(r'^edit_words/?$', 'editWords'),
)
