from django.contrib import admin
from sequences.models import Sequence, Cue, Manifest, ManifestGroup

class SequenceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Sequence, SequenceAdmin)

class CueAdmin(admin.ModelAdmin):
    list_display = ('slug', 'start', 'end',)
    list_filter = ('manifests',)

admin.site.register(Cue, CueAdmin)

class ManifestAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    list_filter = ('windows', 'assets',)

admin.site.register(Manifest, ManifestAdmin)

class ManifestGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_filter = ('manifests', 'persistant',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(ManifestGroup, ManifestGroupAdmin)
