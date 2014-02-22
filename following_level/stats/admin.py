# -*- coding: utf-8 -*-
from django.contrib import admin

from stats.models import Page, Visit

class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'visit_number', 'see_page_date',)
    list_filter = ('url',)
    search_fields = ['url', 'visit_number']

class VisitAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'visit_date', 'internaute',)
    list_filter = ('ip_address',)
    search_fields = ['ip_address', 'internaute__user__username']

admin.site.register(Page, PageAdmin)
admin.site.register(Visit, VisitAdmin)
