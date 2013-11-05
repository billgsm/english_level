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
