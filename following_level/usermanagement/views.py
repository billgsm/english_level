# -*- coding: utf-8 -*-

import logging

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.forms.models import inlineformset_factory

from usermanagement.models import Internaute
from usermanagement.forms import *

logger = logging.getLogger(__name__)

def editProfile(request):
    saved = None
    profile_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            }
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                instance=request.user.internaute, error_class=DivErrorList)
        if form.is_valid():
            user = request.user
            internaute = request.user.internaute

            if form.cleaned_data['avatar'] and \
                    str(form.cleaned_data['avatar']) not in internaute.avatar.name:
                internaute.avatar = form.cleaned_data['avatar']
                saved = True
            if user.last_name != form.cleaned_data['last_name'] and \
                    form.cleaned_data['last_name']:
                user.last_name = form.cleaned_data['last_name']
                if not saved:
                    saved = True
            if user.first_name != form.cleaned_data['first_name'] and \
                    form.cleaned_data['first_name']:
                user.first_name = form.cleaned_data['first_name']
                if not saved:
                    saved = True
            if saved:
                user.save()
                internaute.user = user
                internaute.save()

            return HttpResponseRedirect(reverse('edit_profile'))
        else:
            saved = False

    else:
        form = ProfileForm(initial=profile_data)
    return render(request, "usermanagement/edit_profile.html",
            {
                "form": form,
                "saved": saved
            })

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
      return HttpResponseRedirect(reverse('list', kwargs={'page': 1}))
    else:
      error = True
  else:
    registerform = RegisterForm()
  return render(request, 'usermanagement/register.html', locals())

#@cache_page(60 * 15)
def user_login(request):
  error = False
  if request.user.is_authenticated():
      return HttpResponseRedirect(reverse('list', kwargs={'page': 1}))
  if request.method == 'POST':
    loginform = LoginForm(request.POST)
    if loginform.is_valid():
      username = loginform.cleaned_data["username"]
      password = loginform.cleaned_data["password"]
      user = authenticate(username=username, password=password)
      if user:
        login(request, user)
        return HttpResponseRedirect(reverse('list', kwargs={'page': 1}))
      else:
        error = True
  else:
    loginform = LoginForm()
  return render(request, 'usermanagement/login.html', locals())

def user_logout(request):
    logout(request)
    return redirect(reverse(user_login))
