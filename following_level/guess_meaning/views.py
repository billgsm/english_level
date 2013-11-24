# -*- coding: utf-8 -*-
import json
import logging
from base64 import b64encode, b64decode

from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect

from guess_meaning.models import GuessMeaning
from dydict.models import Dict

class CreateGuessMeaning(CreateView):
    model = GuessMeaning

    def get_context_data(self, **kwargs):
        context = super(CreateGuessMeaning, self).get_context_data(**kwargs)
        dicts_to_guess = Dict.objects.filter(internaute__user=self.request.user)[:10]
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
                guessed_dict = Dict.objects.get(internaute__user=request.user,
                        pk=request.POST['hidden'])
            except Dict.DoesNotExist:
                pass
            else:
                if request.is_ajax():
                    data = {'ack': 'Fail :(',
                            'right_anwser': guessed_dict.word
                            }
                    if request.POST['word_try'] == guessed_dict.word:
                        data = {'ack': 'Success :)'}
                    return HttpResponse(json.dumps(data), mimetype="application/json")
        return HttpResponseRedirect(reverse('guess'))
