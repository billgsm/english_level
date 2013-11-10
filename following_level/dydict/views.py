# -*- coding: utf-8 -*-
import logging
from math import ceil

from django.core.exceptions import ObjectDoesNotExist as DoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.utils.encoding import smart_unicode
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from usermanagement.models import Internaute
from dydict.models import Dict
from dydict.forms import WordForm

logger = logging.getLogger(__name__)

class StaticTemplateView(TemplateView):
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(StaticTemplateView, self).dispatch(*args, **kwargs)


class AboutView(StaticTemplateView):
  template_name = 'dydict/about.html'


class HelpView(StaticTemplateView):
  template_name = 'dydict/help.html'


#@login_required
#def listWords(request):
#  """
#  Send information to template:
#  * page number
#  * word to display
#  * word's indexes
#  * all words for autocompletion purpose
#  * a word was saved
#  """
#  #messages.info(request, u'test message')
#  word_saved = False
#  try:
#    user = Internaute.objects.get(user=request.user)
#  except(MultipleObjectsReturned, DoesNotExist):
#    logger.critical('{0} is not found'.format(request.user.username))
#    # these are impossible cases
#    return HttpResponseRedirect('/dictionary/show_words/')
#  words = Dict.objects.filter(internaute=user).order_by('-last_update', '-rank')
#  requested_page = row_number = 1
#  word_keys = Dict.objects.values('word').exclude(internaute=user).distinct()
#  if request.method == 'POST':
#    if 'row' in request.POST:
#      row_number = int(request.POST['row'])
#    word_form = WordForm(request.POST)
#    if word_form.is_valid():
#      word = word_form.cleaned_data['word']
#      definition = word_form.cleaned_data['definition']
#      user_def = word_form.cleaned_data['user_def']
#      word_ref = word_form.cleaned_data['word_ref']
#      new_word = Dict(word=word, definition=definition, user_def=user_def,
#                      word_ref=word_ref, internaute=user)
#      word_saved = True
#      new_word.save()
#      # Clear fields
#      return HttpResponseRedirect('/dictionary/show_words/')
#  else:
#    word_form = WordForm()
#
#  words_page = Paginator(words[:50], row_number*6, 0, True)
#  num_pages = words_page.num_pages
#  if request.method == 'GET':
#    if 'page' in request.GET and request.GET and \
#            int(request.GET['page']) <= num_pages:
#      requested_page = int(request.GET['page'])
#    elif 'research' in request.GET:
#      import pdb; pdb.set_trace()
#      requested_page = [page.num_pages for page in words_page if request.GET['research'] in page.object_list]
#
#  requested_page = requested_page if requested_page in range(1, num_pages + 1) \
#                             else 1
#  page_list = words_page.page(requested_page).object_list
#  page_list = [ w for w in page_list if w.rank != 0 ]
#  if not page_list:
#    logger.info('<{0}> has no word to display!'.format(user.user.username))
#  word_form = word_form
#  word_saved = word_saved
#  word_keys = [ x['word'].encode('ascii', 'ignore') for x in word_keys ]
#
#  tpl_vars = {'user': request.user,
#              'row_number': row_number,
#              'num_pages': range(int(ceil(words_page.num_pages/float(row_number)))),
#              'current_page': requested_page,
#              'word_form': word_form,
#              'words': page_list,
#              'word_keys': word_keys,
#              'word_saved': word_saved}
#
#  if word_saved:
#    tpl_vars['word'] = word
#
#  return render(request, 'dydict/list_words.html', tpl_vars)

class Word_List(ListView):
  paginate_by = 10
  # Parameter's name excpected in the query request.GET
  # page is the value by default
  page_kwarg = 'page'

  def paginate_queryset(self, queryset, page_size):
      """
      Paginate the queryset, if needed.
      """
      paginator = self.get_paginator(queryset, page_size, allow_empty_first_page=self.get_allow_empty())
      page_kwarg = self.page_kwarg
      page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
      try:
          page_number = int(page)
      except ValueError:
          if page == 'last':
              page_number = paginator.num_pages
          else:
              raise Http404(_("Page is not 'last', nor can it be converted to an int."))
      try:
          page = paginator.page(page_number \
              if page_number <= paginator.num_pages \
              else paginator.num_pages
              )
          return (paginator, page, page.object_list, page.has_other_pages())
      except InvalidPage as e:
          raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                              'page_number': page_number,
                              'message': str(e)
          })

  def get_queryset(self):
    print self.request.user
    words = Dict.objects.filter(internaute__user=self.request.user) \
                        .order_by('-last_update', '-rank')
    if 'query' in self.request.GET and self.request.GET['query']:
      words = words.filter(word__contains=self.request.GET['query'])
    return words

class CreateDict(CreateView):
  model = Dict
  form_class = WordForm

  def post(self, request, *args, **kwargs):
    form = WordForm(request.POST)
    if form.is_valid():
      save_dict = form.save(commit=False)
      save_dict.internaute = Internaute.objects.get(user=request.user)
      save_dict.save()
      return HttpResponseRedirect(reverse('details', args=[save_dict.pk]))
    return render(request, 'dydict/dict_form.html', {'form': form})
