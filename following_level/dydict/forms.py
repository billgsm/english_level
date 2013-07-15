#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from dydict.models import Internaute, Dict

class WordForm(forms.Form):
    """Word fields"""

    word = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={'id': 'put_word',
                                      'placeholder': 'The word',
                                      'x-webkit-speech': True,
                                      'required': "true",
                                      'data-provide': 'typeahead',
                                      'autocomplete': "off",
                                      }))
    definition = forms.CharField(max_length=500,
        widget=forms.TextInput(attrs={'placeholder': 'Definition',
                                      'required': "true"}))
    user_def = forms.CharField(max_length=500,
        widget=forms.TextInput(attrs={'placeholder': 'My definition',
                                      'required': "true"}))
    word_ref = forms.CharField(max_length=500,
        widget=forms.TextInput(attrs={'placeholder': 'The source',
                                      'required': "true"}))
    #definition = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-xlarge', 'rows': '8', 'placeholder': 'definitions, examples ...'}))
    #Should figure out why clean_word doesn't work and show up a syntax error o_O
    def clean(self):
        cleaned_data = super(WordForm, self).clean()
        exists = Dict.objects.filter(word=cleaned_data.get('word'))
        if not cleaned_data.get('word') or ' ' in cleaned_data.get('word') or exists or not cleaned_data.get('definition'):
            msg_word = u'You should enter a word with no white space'
            self._errors['word'] = self.error_class([msg_word])
        return cleaned_data

class RegisterForm(forms.Form):
    """Registration fields"""

    username = forms.CharField(max_length=40,
                   widget=forms.TextInput(attrs={'placeholder': 'login',
                                                 'required': "true"}))
    password = forms.CharField(max_length=100,
                   widget=forms.PasswordInput(attrs={'placeholder': '*********',
                                                     'required': "true"}))
    re_password = forms.CharField(max_length=100,
                      widget=forms.PasswordInput(attrs={'placeholder': '*********',
                                                        'required': "true"}))
    email = forms.EmailField(max_length=100,
            widget=forms.TextInput(attrs={'placeholder': 'email',
                                          'required': "true"}))


class LoginForm(forms.Form):
    """Login fields"""
    username = forms.CharField(label="Login", max_length=30,
                   widget=forms.TextInput(attrs={'placeholder': 'login',
                                                 'required': "true"}))
    password = forms.CharField(label="Password",
                   widget=forms.PasswordInput(attrs={'placeholder': '*********',
                                                     'required': "true"}))
