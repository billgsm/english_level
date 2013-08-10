# -*- coding: utf-8 -*-
from django.db import models

class DebugData(models.Model):
  msg_level = models.CharField(max_length=50, default='NULL')
  msg = models.TextField(default='NULL')
  full_debug = models.TextField(default='NULL')
  last_update = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="creation date")

  def __unicode__(self):
    return u"%s" % self.info_type
