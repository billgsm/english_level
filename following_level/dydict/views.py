# -*- coding: utf-8 -*-
import hashlib

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from dydict.models import *
from dydict.forms import *


class StaticTemplateView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StaticTemplateView, self).dispatch(*args, **kwargs)


class AboutView(StaticTemplateView):
    template_name = 'dydict/about.html'


class HelpView(StaticTemplateView):
    template_name = 'dydict/help.html'


@login_required
def listWords(request):
    if request.user.is_authenticated():
        try:
            internaute = Internaute.objects.get(id=request.user.id)
        except DoesNotExist:
            pass
        words = internaute.dictionary.all()

    if request.method == 'POST':
        word_form = WordForm(request.POST)
        if word_form.is_valid():
            hash_def = hashlib.md5(word_form.cleaned_data['definition']).hexdigest()
            word = word_form.cleaned_data['word']
            definition = word_form.cleaned_data['definition']
            new_word = Dict(word=word,
                            definition=definition,
                            hash_definition=hash_def)
            new_word.save()
            internaute.dictionary.add(new_word)
    else:
        word_form = WordForm()

    return render(request, 'dydict/list_words.html', locals())

def createUser(request):
    loginform = LoginForm()
    if request.method == 'POST':
        register = RegisterForm(request.POST)
        if register.is_valid():
            login = register.cleaned_data['login']
            email = register.cleaned_data['email']
            hash_password = hashlib.sha224(register.cleaned_data['password']).hexdigest()
            student = Internaute(
                login=login,
                password=hash_password,
                email=email,
            )
            student.save()
            request.session['reference'] = student.id
            return HttpResponseRedirect('/dictionary/show_words/')
    else:
        register = RegisterForm()
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
    return render(request, 'dydict/register.html', locals())

def user_logout(request):
    logout(request)
    return redirect(reverse(user_login))
