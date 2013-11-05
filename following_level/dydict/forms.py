#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from dydict.models import Dict

class WordForm(forms.ModelForm):
  class Meta:
    model = Dict
    exclude = ('rank', 'visibility', 'internaute', 'last_update',)
