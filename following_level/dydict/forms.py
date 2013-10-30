#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from dydict.models import Dict

class WordForm(forms.ModelForm):
  class Meta:
    model = Dict
    exclude = ('rank', 'visibility', 'internaute', 'last_update',)

class RegisterForm(forms.Form):
    """Registration fields"""
    username = forms.CharField(label="", max_length=40,
                   widget=forms.TextInput(attrs={'placeholder': 'login',
                                                 'class': 'input-block-level',
                                                 'required': "true"}))
    password = forms.CharField(label="", max_length=100,
                   widget=forms.PasswordInput(attrs={'placeholder': 'password',
                                                     'class': 'input-block-level',
                                                     'required': "true"}))
    re_password = forms.CharField(label="", max_length=100,
                      widget=forms.PasswordInput(attrs={'placeholder': 're-password',
                                                        'class': 'input-block-level',
                                                        'required': "true"}))
    email = forms.EmailField(label="", max_length=100,
            widget=forms.TextInput(attrs={'placeholder': 'email',
                                           'class': 'input-block-level',
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
