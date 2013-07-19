# -*- coding: utf-8 -*-
from random import randint

from django.utils.encoding import smart_unicode
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib import messages

from dydict.models import Internaute
from dydict.forms import *
import get_words


class StaticTemplateView(TemplateView):
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(StaticTemplateView, self).dispatch(*args, **kwargs)


class AboutView(StaticTemplateView):
  template_name = 'dydict/about.html'


class HelpView(StaticTemplateView):
  template_name = 'dydict/help.html'


@login_required
def listWords(request, page_number=1):
  #messages.info(request, u'test message')
  user = Internaute.objects.get(user=request.user)
  word_saved = False
  words = Paginator(Dict.objects.filter(internaute=user)
                        .order_by('-last_update', '-rank')[:50], 5, 3, True)
  word_keys = Dict.objects.values('word').distinct()
  if request.method == 'POST':
    word_form = WordForm(request.POST)
    if word_form.is_valid():
      word = smart_unicode(word_form.cleaned_data['word'])
      definition = smart_unicode(word_form.cleaned_data['definition'])
      user_def = smart_unicode(word_form.cleaned_data['user_def'])
      word_ref = smart_unicode(word_form.cleaned_data['word_ref'])
      new_word = Dict(word=word,
                      definition=definition,
                      user_def=user_def,
                      word_ref=word_ref,
                      internaute=user)
      new_word.save()
      word_saved = True
      # Clear fields
      word_form = WordForm()
  else:
    word_form = WordForm()

  tpl_dict = {
      'user': user,
      'word_form': word_form,
      'words': words,
      'word_saved': word_saved,
      'word_keys': word_keys}

  if word_saved:
    tpl_dict['word'] = word

  words_page = tpl_dict["words"]
  num_pages = words_page.num_pages
  page_number = int(page_number)
  current_page = page_number if page_number in range(1, num_pages + 1) \
                             else 1
  word_index = (current_page - 1) * 5
  page_list = words_page.page(current_page).object_list
  page_list = [ w for w in page_list if w.rank != 0 ]
  word_form = tpl_dict["word_form"]
  word_saved = tpl_dict["word_saved"]
  word_keys = [ x['word'].encode('ascii', 'ignore') for x in tpl_dict["word_keys"] ]

  tpl_vars = {'user': request.user,
              'num_pages': words_page.num_pages,
              'current_page': current_page,
              'word_form': word_form,
              'words': page_list,
              'word_keys': word_keys,
              'word_index': word_index,
              'word_saved': word_saved}

  if word_saved:
    tpl_vars['word'] = tpl_dict["word"]

  return render(request, 'dydict/list_words.html', tpl_vars)

def createUser(request):
  error = False
  if request.method == 'POST':
    registerform = RegisterForm(request.POST)
    if registerform.is_valid():
      username = registerform.cleaned_data['username']
      email = registerform.cleaned_data['email']
      password = registerform.cleaned_data['password']
      user = User.objects.create_user(username=username,
                  email=email,
                  password=password)

      internaute = Internaute(user=user)
      internaute.save()
      user = authenticate(username=username, password=password)
      login(request, user)
      return HttpResponseRedirect('/dictionary/show_words/')
  else:
    registerform = RegisterForm()
  return render(request, 'dydict/register.html', locals())

#@cache_page(60 * 15)
def user_login(request):
  error = False
  if request.method == 'POST':
    loginform = LoginForm(request.POST)
    if loginform.is_valid():
      username = loginform.cleaned_data["username"]
      password = loginform.cleaned_data["password"]
      user = authenticate(username=username, password=password)
      if user:
        login(request, user)
        return HttpResponseRedirect('/dictionary/show_words/')
      else:
        error = True
  else:
    loginform = LoginForm()
  return render(request, 'dydict/login.html', locals())

def user_logout(request):
  logout(request)
  return redirect(reverse(user_login))
