#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList

from usermanagement.models import Internaute


class GuessForm(forms.Form):
    word = forms.CharField(label="", max_length=250, required=True,
                   widget=forms.TextInput(
                       attrs={
                           'placeholder': 'Guess the meaning',
                           'name': 'word',
                           'class': 'word',
                           'value': '',
                           'required': True,
                           'id': ''
                           }
                       ))
