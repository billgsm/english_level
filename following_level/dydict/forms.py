# -*- coding: utf-8 -*-
from django import forms
from dydict.models import Internaute, Dict
import hashlib

class WordForm(forms.Form):
    ###########################################
    ###############Word fields#################
    ###########################################
    word = forms.CharField(max_length=50)
    definition = forms.CharField(widget=forms.Textarea)

#Should figure out why clean_word doesn't work and show up a syntax error o_O
    def clean(self):
        cleaned_data = super(WordForm, self).clean()
        exists = Dict.objects.filter(word=cleaned_data['word'])
        if not cleaned_data['word'] or ' ' in cleaned_data['word'] or exists or not cleaned_data['definition']:
            msg_word = u'You should enter a word with no white space'
            self._errors['login'] = self.error_class([msg_word])
            del cleaned_data['word']
            del cleaned_data['definition']
        return cleaned_data
    #def clean_word(self):
    #    word = self.cleaned_data['word']
    #    if not word:
    #    return word

class RegisterForm(forms.Form):
    ###########################################
    ######Registration fields##################
    ###########################################
    login = forms.CharField(max_length=40)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(max_length=100)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        user_exists = Internaute.objects.filter(login=cleaned_data['login'])
        email_exists = Internaute.objects.filter(email=cleaned_data['email'])
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
    ###########################################
    ###############Login fields################
    ###########################################
    name = forms.CharField(max_length=40)
    passwd = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        name = cleaned_data.get('name')
        passwd = cleaned_data.get('passwd')
        msg = u"This field is mandotary"
        if not name:
            self._errors['name'] = self.error_class([msg])
        elif not passwd:
            self._errors['passwd'] = self.error_class([msg])
        else:
            passwd_hash = hashlib.sha224(passwd).hexdigest()
            user_exists = Internaute.objects.filter(login=name)
            if not user_exists:
                msg = u"This user doesn't exist."
                self._errors['name'] = self.error_class([msg])
                del cleaned_data['name']
                del cleaned_data['passwd']
            else:
                user_password = user_exists[0].password
                if user_password != passwd_hash:
                    msg = u"Wrong information."
                    self._errors['name'] = self._errors['passwd'] = self.error_class([msg])
                    del cleaned_data['name']
                    del cleaned_data['passwd']


        return cleaned_data
