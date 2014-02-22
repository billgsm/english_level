#-*- coding: utf-8 -*-
from models import Page, Visit
from dydict.models import Internaute

class StatsMiddleware(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    if not request.user.is_superuser:
        try:
          page = Page.objects.get(url__contains=request.path)
          page.visit_number += 1
          page.save()
        except Page.DoesNotExist:
          page = Page(url=request.path).save()

    if not request.user.is_anonymous() and not request.user.is_superuser:
      user = Internaute.objects.get(user=request.user)
      try:
        visit = Visit.objects.get(internaute=user,
            ip_address=request.META['REMOTE_ADDR'])
      except Visit.DoesNotExist:
        Visit(internaute=user,
              ip_address=request.META['REMOTE_ADDR']).save()
