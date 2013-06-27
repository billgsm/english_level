#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from dydict.models import Internaute, Dict

class WordForm(forms.Form):
    """Word fields"""

    word = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'placeholder': 'word'}))
    definition = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-xlarge', 'rows': '8', 'placeholder': 'definitions, examples ...'}))
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

    login = forms.CharField(max_length=40,
                            widget=forms.TextInput(attrs={'placeholder': 'login'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': '*********'}))
    re_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': '*********'}))
    email = forms.EmailField(max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'email'}))
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        user_exists = Internaute.objects.filter(login=cleaned_data.get('login'))
        email_exists = Internaute.objects.filter(email=cleaned_data.get('email'))
        if user_exists:
            msg_login = u"Login already used."
            self._errors['login'] = self.error_class([msg_login])
            del cleaned_data['login']
        if email_exists:
            msg_email = u"Email already registered"
            self._errors['email'] = self.error_class([msg_email])
            del cleaned_data['email']
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        if password != re_password:
            msg = u"Please enter your password twice"
            self._errors['password'] = self.error_class([msg])
            self._errors['re_password'] = self.error_class([msg])
            del cleaned_data['password']
            del cleaned_data['re_password']
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Login", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
