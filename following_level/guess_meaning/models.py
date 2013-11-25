from django.db import models

from dydict.models import Dict

class GuessMeaning(models.Model):
    result = models.IntegerField(null=True)
    dict_to_guess = models.ForeignKey(Dict)
    created_date = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Creation date")

    def __unicode__(self):
        return u'{0} -> {1}'.format(self.dict_to_guess, self.result)
