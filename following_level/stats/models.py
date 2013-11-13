from django.db import models

from dydict.models import Internaute


class Page(models.Model):
  url = models.URLField()
  visit_number = models.IntegerField(default=1)
  see_page_date = models.DateTimeField(auto_now_add=True,
                    verbose_name="The date when this page was visited")

  def __unicode__(self):
    return u'{0}'.format(self.url)


class Visit(models.Model):
  ip_address = models.IPAddressField()
  visit_date = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="Visit date")
  internaute = models.ForeignKey(Internaute)

  def __unicode__(self):
    return u'{0}'.format(self.ip_address)
