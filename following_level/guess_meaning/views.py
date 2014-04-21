# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
import datetime
from itertools import chain, izip_longest
import json
import logging

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from forms import *
from dydict.models import Dict

def createGuessMeaning(request):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    dicts = Dict.objects.filter(Q(internaute__user=request.user) &
            Q(last_update__lt=tomorrow))[:10]

    if request.method == 'POST':
        if request.is_ajax():
            form = GuessForm(request.POST)
            if form.is_valid():
                try:
                    dict_data = Dict.objects.get(internaute__user=request.user,
                            pk=request.POST['hidden'])
                except Dict.DoesNotExist:
                    # Have to log this
                    return HttpResponseRedirect(reverse('guess'))
                else:
                    data = {'ack': 'Fail :(',
                            'right_anwser': dict_data.word
                            }
                    if form.cleaned_data['word'] == dict_data.word:
                        data = {'ack': 'Success :)'}
                        dict_data.rank += 1
                    else:
                        dict_data.rank = 0
                    dict_data.save()
                    return HttpResponse(json.dumps(data),
                            mimetype="application/json")

    if request.method == 'GET':
        form = GuessForm()
        return render(request, "guess_meaning/guessmeaning_form.html",
                    {
                        "form": form,
                        "dicts": dicts
                    })
