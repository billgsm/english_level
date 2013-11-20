from django.contrib import admin

from models import Dict

class DictAdmin(admin.ModelAdmin):
    list_display = ('word', 'definition', 'user_def', 'word_ref',)
    search_fields = ['word', 'definition', 'user_def', 'word_ref']

admin.site.register(Dict, DictAdmin)
