#-*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.util import ErrorList

from usermanagement.models import Internaute


MAX_UPLOAD_SIZE = 4*1024*1024

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u''
        return u'<ul class="errorlist alert alert-error">%s</ul>' % \
                    ''.join([u'<li class="error">%s</li>' % e for e in self])


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="", max_length=40,
                   required=False,
                   widget=forms.TextInput(
                       attrs={'placeholder': 'first_name'}
                       ))
    last_name = forms.CharField(label="", max_length=40,
                   required=False,
                   widget=forms.TextInput(
                       attrs={'placeholder': 'last_name'}
                       ))
    password = forms.CharField(label="", max_length=100,
            required=False,
            widget=forms.PasswordInput(
                attrs={'placeholder': 'password'}
                        ))
    email = forms.EmailField(label="", max_length=100,
            required=False,
            widget=forms.TextInput(attrs={'placeholder': 'email'}))

    avatar = forms.ImageField(label="", required=False)

    class Meta:
        model = Internaute
        exclude = ('user', 'level', 'avatar',)

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar', False)
        if image:
            if image._size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Image's too large ( > 4MB )")
            return image
        # Supposed to happen when no image is uploaded
        #else:
        #    raise ValidationError("Couldn't read uploaded image")

    def save(self, commit=True):
        super(ProfileForm, self).save(commit=commit)


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
