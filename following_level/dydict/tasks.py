# -*- coding: utf-8 -*-
from celery import task

from dydict.models import Dict, Internaute
from dydict.forms import *

@task()
def save_word(word_args):
  new_word = Dict(word=word_args[0], definition=word_args[1], user_def=word_args[2],
                  word_ref=word_args[3], internaute=word_args[4])
  new_word.save()
