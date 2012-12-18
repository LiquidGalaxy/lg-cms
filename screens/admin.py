from django.contrib import admin
from screens.models import Window, Screen

class ScreenAdmin(admin.ModelAdmin):
    list_display = ('slug', 'width', 'height',)

admin.site.register(Screen, ScreenAdmin)

class WindowAdmin(admin.ModelAdmin):
    list_display = ('slug', 'screen', 'window_type',)
    list_filter = ('screen', 'window_type',)

admin.site.register(Window, WindowAdmin)

