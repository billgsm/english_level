#-*- coding: utf-8 -*-
from django import forms

class WordForm(forms.Form):
    """Word fields"""

    word = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={'id': 'word',
                                      'placeholder': 'The word',
                                      'x-webkit-speech': True,
                                      'required': "true",
                                      'disabled': "true",
                                      'autocomplete': "off",
                                      'background-color': 'rgba(72,72,72, 0.4);',
                                      }))
    definition = forms.CharField(max_length=500,
        widget=forms.TextInput(attrs={'placeholder': 'Definition',
                                      'required': "true",
                                      'autocomplete': "off",
                                      }))
    user_def = forms.CharField(max_length=500,
        widget=forms.TextInput(attrs={'placeholder': 'My definition',
                                      'required': "true",
                                      'autocomplete': "off",
                                      }))
    word_ref = forms.CharField(max_length=500,
        widget=forms.TextInput(attrs={'placeholder': 'The source',
                                      'required': "true",
                                      'autocomplete': "off",
                                      }))
