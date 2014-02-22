# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate

from usermanagement.models import Internaute
from usermanagement.forms import *


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
