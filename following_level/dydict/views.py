# -*- coding: utf-8 -*-
import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from dydict.models import *
from dydict.forms import *


def listWords(request):
    try:
        user = Internaute.objects.filter(id=request.session['reference'])[0]
        user_name = user.login
        words = user.dictionary.all()
    except KeyError:
        return HttpResponseRedirect('/dictionary/login/')

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
            user.dictionary.add(new_word)
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

def login(request):
    register = RegisterForm()
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            login = loginform.cleaned_data['name']
            request.session['reference'] = Internaute.objects.filter(login=login)[0].id
            return HttpResponseRedirect('/dictionary/show_words/')
    else:
        loginform = LoginForm()
    return render(request, 'dydict/register.html', locals())

def logout(request):
    if request.method == 'POST':
        try:
            del request.session['reference']
        except KeyError:
            pass
        return HttpResponseRedirect('/dictionary/login/')
    return HttpResponseRedirect('/dictionary/show_words/')
