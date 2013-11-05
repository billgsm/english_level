# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Internaute(models.Model):
  user = models.OneToOneField(User)
  level = models.IntegerField(default=0)
  last_update = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="creation date")

  def __unicode__(self):
    return u"%s" % self.user


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

  >>> from dydict.models import Internaute, Dict
  >>> from django.contrib.auth.models import User
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
  definition = models.TextField()
  user_def= models.TextField()
  word_ref = models.TextField()
  rank = models.PositiveSmallIntegerField(default=1)
  visibility = models.BooleanField(default=True)
  last_update = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="creation date")
  internaute = models.ForeignKey(Internaute)

  def __unicode__(self):
    return u"%s" % self.word

  def get_absolute_url(self):
    """
    * The method name will be used by django
    """
    return reverse("details", kwargs={"pk": self.pk})
