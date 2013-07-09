# -*- coding: utf-8 -*-
import hashlib

from celery import task
from django.utils.encoding import smart_unicode, smart_str

from dydict.models import *
from dydict.forms import *

@task()
def words(user, post, methode):
    if user.is_authenticated():
        try:
            internaute = Internaute.objects.get(id=user.id)
        except DoesNotExist:
            pass
        words = internaute.dictionary.all()

    if methode == 'POST':
        word_form = WordForm(post)
        if word_form.is_valid():
            hash_def = hashlib.md5(smart_str(word_form.cleaned_data['definition'])).hexdigest()
            word = smart_unicode(word_form.cleaned_data['word'])
            definition = smart_unicode(word_form.cleaned_data['definition'])
            new_word = Dict(word=word,
                            definition=definition,
                            hash_definition=hash_def)
            new_word.save()
            internaute.dictionary.add(new_word)
            # Clear fields
            word_form = WordForm()
    else:
        word_form = WordForm()

    return {'user': user,
            'word_form': word_form,
            'words': words}
