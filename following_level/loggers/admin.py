# -*- coding: utf-8 -*-
from django.contrib import admin

from loggers.models import DebugData

class LoggersAdmin(admin.ModelAdmin):
    list_display = ('msg_level', 'msg', 'full_debug',)
    list_filter = ('msg_level',)
    search_fields = ['full_debug']

admin.site.register(DebugData, LoggersAdmin)
