from django.conf.urls import patterns, url

urlpatterns = patterns('manage_word.views',
    url(r'^remove_words/?$', 'removeWords'),
    #url(r'^remove_words/(?P<word>\w+)/?$', 'removeWords'),
    #url(r'^show_words/(?P<page_number>\d{1})/?$', 'listWords'),
)
