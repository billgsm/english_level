#-*- coding: utf-8 -*-
from models import Page, Visit
from dydict.models import Internaute

class StatsMiddleware(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    try:
      page = Page.objects.get(url__contains=request.path)
      page.visit_number += 1
      page.save()
    except Page.DoesNotExist:
      page = Page(url=request.path).save()

    if not request.user.is_anonymous():
      user = Internaute.objects.get(user=request.user)
      try:
        visit = Visit.objects.get(internaute=user,
            ip_address=request.META['REMOTE_ADDR'])
      except Visit.DoesNotExist:
        Visit(internaute=user,
              ip_address=request.META['REMOTE_ADDR']).save()

  def process_response(self, request, response):
    if response.status_code == 200:
      p = Page.objects.get(url=request.path)
      response.content += u"""\
          This page has been seen {0} times.""".format(p.visit_number)
    return response
