#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

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
    #Should figure out why clean_word doesn't work and show up a syntax error o_O
    def clean(self):
        cleaned_data = super(WordForm, self).clean()
        if not cleaned_data.get('word') or \
           not cleaned_data.get('definition') or \
           not cleaned_data.get('user_def') or \
           not cleaned_data.get('word_ref'):
            msg_word = u'You should fill all these fields'
            self._errors['word'] = self.error_class([msg_word])
        return cleaned_data

class RegisterForm(forms.Form):
    """Registration fields"""
    username = forms.CharField(label="", max_length=40,
                   widget=forms.TextInput(attrs={'placeholder': 'login',
                                                 'required': "true"}))
    password = forms.CharField(label="", max_length=100,
                   widget=forms.PasswordInput(attrs={'placeholder': 'password',
                                                     'required': "true"}))
    re_password = forms.CharField(label="", max_length=100,
                      widget=forms.PasswordInput(attrs={'placeholder': 're-password',
                                                        'required': "true"}))
    email = forms.EmailField(label="", max_length=100,
            widget=forms.TextInput(attrs={'placeholder': 'email',
                                          'required': "true"}))
    def clean(self):
      cleaned_data = super(RegisterForm, self).clean()
      if (User.objects.filter(username=cleaned_data.get('username'))) or \
         (User.objects.filter(email=cleaned_data.get('email'))):
         msg_word = u'This user/email already exists!!'
         self._errors['word'] = self.error_class([msg_word])
      return cleaned_data


class LoginForm(forms.Form):
    """Login fields"""
    username = forms.CharField(label="", max_length=30,
                   widget=forms.TextInput(attrs={'placeholder': 'Login or email',
                                                 'class': 'input-block-level',
                                                 'required': "true"}))
    password = forms.CharField(label="",
                   widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                     'class': 'input-block-level',
                                                     'required': "true"}))
