from django.contrib import admin
from sequences.models import Sequence, Cue

class SequenceAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Sequence, SequenceAdmin)

class CueAdmin(admin.ModelAdmin):
    list_display = ('slug', 'start', 'end',)
    list_filter = ('windows', 'assets',)

admin.site.register(Cue, CueAdmin)
