# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Dict(models.Model):
  word = models.CharField(max_length=50,
                          unique=True)
  definition = models.TextField()
  hash_definition = models.CharField(max_length=255,
                                     unique=True)
  last_update = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="creation date")

  def __unicode(self):
    return u"%s" % self.word


class Internaute(models.Model):
  user = models.OneToOneField(User)
  level = models.IntegerField(default=0)
  last_update = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="creation date")
  dictionary = models.ManyToManyField(Dict)

  def __unicode(self):
    return u"%s" % self.login
