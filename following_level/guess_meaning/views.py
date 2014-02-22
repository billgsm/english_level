# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
from itertools import chain, izip_longest
import json
import logging

from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect

from guess_meaning.models import GuessMeaning
from dydict.models import Dict

class CreateGuessMeaning(CreateView):
    model = GuessMeaning

    def get_context_data(self, **kwargs):
        context = super(CreateGuessMeaning, self).get_context_data(**kwargs)
        dicts_to_guess = Dict.objects.filter(internaute__user=self.request.user,
                visibility=True)[:10]
        for dict_to_guess in dicts_to_guess:
            try:
                GuessMeaning.objects.get(dict_to_guess=dict_to_guess)
            except GuessMeaning.DoesNotExist:
                GuessMeaning(dict_to_guess=dict_to_guess).save()

        context['dicts_to_guess'] = dicts_to_guess
        return context

    def post(self, request, *args, **kwargs):
        if 'word_try' in request.POST and 'hidden' in request.POST:
            try:
                dict_data = Dict.objects.get(internaute__user=request.user,
                        pk=request.POST['hidden'])
            except Dict.DoesNotExist:
                # Have to log this
                return HttpResponseRedirect(reverse('guess'))
            else:
                if request.is_ajax():
                    data = {'ack': 'Fail :(',
                            'right_anwser': dict_data.word
                            }
                    guessed_word = GuessMeaning.objects.get(dict_to_guess=dict_data)
                    guessed_word.result = 1 if not guessed_word.result \
                                            else guessed_word.result+1
                    if request.POST['word_try'] == dict_data.word:
                        data = {'ack': 'Success :)'}
                        dict_data.visibility = False
                        dict_data.save()
                    else:
                        guessed_word.result = 0
                    guessed_word.save()
                    return HttpResponse(json.dumps(data),
                            mimetype="application/json")

        return HttpResponseRedirect(reverse('guess'))
