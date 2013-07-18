# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Internaute(models.Model):
  user = models.OneToOneField(User)
  level = models.IntegerField(default=0)
  last_update = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="creation date")

  def __unicode__(self):
    return u"%s" % self.user


class Dict(models.Model):
  word = models.CharField(db_index=True, max_length=50)
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
