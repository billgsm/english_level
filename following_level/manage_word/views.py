# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from dydict.models import Dict, Internaute
from manage_word.forms import WordForm

@login_required
def removeWords(request):
  if request.method == 'POST':
    try:
      dict2_remove = Dict.objects.get(
          internaute=Internaute.objects.get(user=request.user),
          word=request.POST['word'])
    except:#Dict.DoesNotExist
      pass
    else:
      dict2_remove.delete()
      return HttpResponse('<h1>{0} removed</h1>'.format(request.POST['word']))

@login_required
def hideWords(request):
  if request.method == 'POST':
    try:
      dict2_hide = Dict.objects.get(
          internaute=Internaute.objects.get(user=request.user),
          word=request.POST['word'])
    except Dict.DoesNotExist:
      pass
    else:
      dict2_hide.rank = 0
      dict2_hide.save()
      return HttpResponse('<h1>{0} removed</h1>'.format(request.POST['word']))

@login_required
def editWords(request, word=None):
  if request.method == 'POST':
    word_form = WordForm(request.POST)
    if word_form.is_valid():
      dict2_edit = Dict.objects.get(
          internaute=Internaute.objects.get(user=request.user),
          word=word_form.cleaned_data['word'])
      dict2_edit.definition = word_form.cleaned_data['definition']
      dict2_edit.user_def = word_form.cleaned_data['user_def']
      dict2_edit.word_ref = word_form.cleaned_data['word_ref']
      dict2_edit.save()
      return HttpResponseRedirect('/dictionary/show_words/')
  try:
    word = word.replace('-', ' ')
    dict2_edit = Dict.objects.get(
        internaute=Internaute.objects.get(user=request.user),
        word=word)
  except (Dict.DoesNotExist):
    pass
  except AttributeError:
    return HttpResponseRedirect('/dictionary/show_words/')
  else:
    word_form = WordForm({'word': dict2_edit.word,
                        'definition': dict2_edit.definition,
                        'user_def': dict2_edit.user_def,
                        'word_ref': dict2_edit.word_ref})

    return render(request, 'manage_word/edit_word.html',
                           {'word_form': word_form})
