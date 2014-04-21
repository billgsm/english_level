# -*- coding: utf-8 -*-
import logging
from math import ceil
import random

from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist as \
                                        DoesNotExist, MultipleObjectsReturned
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.encoding import smart_unicode
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
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


class HelpView(StaticTemplateView):
  template_name = 'dydict/help.html'


def dictList(request, page=1):
    """
    """
    page_obj = {
            'has_next': False,
            'has_previous': False,
            'next_page_number': 1,
            'previous_page_number': 1,
    }

    elements_by_page = 10

    dicts = Dict.objects.filter(internaute__user=request.user)
    words = dicts.exclude(word__contains=' ')
    idioms = dicts.filter(word__contains=' ')
    if request.method == 'GET' and 'query' in request.GET:
        words = words.filter(word__contains=request.GET['query'])
        idioms = idioms.filter(word__contains=request.GET['query'])

    words_ten = Paginator(words, elements_by_page)
    idioms_five = Paginator(idioms, elements_by_page/2)

    try:
        if words_ten.page(page).has_next():
            page_obj['next_page_number'] = int(page) + 1
            page_obj['has_next'] = True
        else:
            page_obj['next_page_number'] = words_ten.num_pages - 1
            page_obj['has_next'] = False

        if words_ten.page(page).has_previous():
            page_obj['previous_page_number'] = int(page) - 1
            page_obj['has_previous'] = True
        else:
            page_obj['previous_page_number'] = 1
            page_obj['has_previous'] = False
    except PageNotAnInteger:
        page = 1
        page_obj['has_next'] = True
    except EmptyPage:
        page = page_obj['next_page_number'] = words_ten.num_pages
        page_obj['has_next'] = True


    words_page = words_ten.page(page)
    idioms_page = idioms_five.page(random.randint(1, idioms_five.num_pages))

    return render(request,
                  'dydict/dict_list.html',
                  {
                      'idioms': idioms_page,
                      'words': words_page,
                      'page_obj': page_obj
                  })


def contactView(request):
    template_name = 'dydict/contact.html'
    if request.method == 'POST' and 'new_message' in request.POST:
        msg = request.POST['new_message'].strip()
        if msg:
            send_mail('From ' + request.user.username, msg,
                      'admin@alwaysdata.fr',
                      [settings.ADMINS[0][1]], fail_silently=False)
    return render(request, template_name, locals())


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
