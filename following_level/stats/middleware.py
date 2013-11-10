#-*- coding: utf-8 -*-
from models import Page

class StatsMiddleware(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    try:
      p = Page.objects.get(url=request.path)
      p.visit_number += 1
      p.save()
    except Page.DoesNotExist:
      Page(url=request.path).save()

  def process_response(self, request, response):
    if response.status_code == 200:
      p = Page.objects.get(url=request.path)
      #response.content += u"""This page has been seen \
      #    {0} times.""".format(p.visit_number)
    return response
