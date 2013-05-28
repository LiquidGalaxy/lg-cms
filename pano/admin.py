from django.contrib import admin
from models import Panorama, PanoramaGroup

class PanoramaAdmin(admin.ModelAdmin):
    list_display = ('title', 'group')
    list_filter = ('group', 'projection')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Panorama, PanoramaAdmin)

class PanoramaGroupAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(PanoramaGroup, PanoramaGroupAdmin)
