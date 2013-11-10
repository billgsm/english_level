from django.db import models

from usermanagement.models import Internaute

class Page(models.Model):
  url = models.URLField()
  visit_number = models.IntegerField(default=1)
  #ip_address = models.IPAddressField()
  visit_date = models.DateTimeField(auto_now_add=True,
                                     auto_now=True,
                                     verbose_name="Visit date")
  #user = models.OneToOneField(Internaute, blank=True)

  def __unicode__(self):
    return self.url
