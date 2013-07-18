from django.conf.urls import patterns, url

urlpatterns = patterns('manage_word.views',
    url(r'^remove_words/?$', 'removeWords'),
    url(r'^hide_words/?$', 'hideWords'),
    #url(r'^show_words/(?P<page_number>\d{1})/?$', 'listWords'),
)
