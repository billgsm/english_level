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


class ContactView(StaticTemplateView):
  template_name = 'dydict/contact.html'


class HelpView(StaticTemplateView):
  template_name = 'dydict/help.html'


class Word_List(ListView):
    paginate_by = 10
    # Parameter's name excpected in the query request.GET
    # page is the value by default
    page_kwarg = 'page'

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(queryset, page_size,
                allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or \
                           self.request.GET.get(page_kwarg) or \
                           1
        try:
            page_number = int(page) or 1
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
