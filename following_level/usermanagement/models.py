from django.db import models
from django.contrib.auth.models import User


class Internaute(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to="photos/")
    #thumbnail = models.ImageField(upload_to="photos/")
    level = models.IntegerField(default=0)

    def __unicode__(self):
        return u"%s" % self.user
