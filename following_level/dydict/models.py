# -*- coding: utf-8 -*-
from datetime import timedelta, date, datetime

from django.template.defaultfilters import date as django_date
from django.db import models
from django.core.urlresolvers import reverse

from usermanagement.models import Internaute

class Dict(models.Model):
  """
  This table contains all data about word
  - `word`: can be a simple word or many words
  - `definition`: definition of `word`
  - `user_def`: examples using `word`
  - `rank`: score of `word`
  - `visibility`: `internaute` doesn't want to see it any
                  more on his page
  - `last_update`: when was the word modified
  - `internaute`: owner of `word`
  - `get_absolute_url`: built the permanent link of the word
  - `colored_word`: tells whether or not the word was added
                    less than a week ago

  >>> from dydict.models import Dict
  >>> from django.contrib.auth.models import User
  >>> from usermanagement.models import Internaute
  >>> user = User(username="john", password="pass", email="john@msn.fr")
  >>> user.save()
  >>> internaute = Internaute(user=user)
  >>> internaute.save()
  >>> d1 = Dict(word="my word", definition="my definition", user_def="my user_def", word_ref="my word_ref", internaute=internaute)
  >>> d1.save()
  >>> Dict.objects.get(word="my word").definition
  u'my definition'
  """
  word = models.CharField(db_index=True, max_length=250)
  definition = models.TextField(blank=True, null=True)
  user_def= models.TextField(blank=True, null=True)
  word_ref = models.TextField(blank=True, null=True)
  rank = models.PositiveSmallIntegerField(default=0)
  visibility = models.BooleanField(default=True)
  last_update = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="Update date")
  created_date = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Creation date")
  internaute = models.ForeignKey(Internaute)

  def __unicode__(self):
    return u"%s" % self.word

  def get_absolute_url(self):
    """
    * The method name will be used by django
    """
    return reverse("details", kwargs={"pk": self.pk})

  def colored_word(self):
    """
    * New words will be highlighted for a week
    """
    is_new_word = False
    # Loop backwards and stop when it matches
    for i in range(7, -1, -1):
      if datetime.combine(self.last_update + timedelta(days=7-i),
                          datetime.min.time()) >= \
                              datetime.combine(date.today(),
                                               datetime.min.time()):
        return u' btn-custom{0}'.format(i)
    return u''

  # Allow html tags, do not escape them for this function
  colored_word.allow_tags = True
