from django.db import models

from dydict.models import Dict

class GuessMeaning(models.Model):
    status_result = (
        (0, "fail"),
        (1, "success"),
        )
    result = models.IntegerField(choices=status_result, null=True)
    dict_to_guess = models.ForeignKey(Dict)
    created_date = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Creation date")
