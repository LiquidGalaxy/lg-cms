from django.contrib import admin
from geo.models import Bookmark, BookmarkGroup
from geo.forms import BookmarkAdminForm

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'group')
    list_filter = ('group',)
    prepopulated_fields = {'slug': ('title',)}

    form = BookmarkAdminForm

admin.site.register(Bookmark, BookmarkAdmin)

class BookmarkGroupAdmin(admin.ModelAdmin):
    list_display = ('title',)
    # list_filter = ('group',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(BookmarkGroup, BookmarkGroupAdmin)
