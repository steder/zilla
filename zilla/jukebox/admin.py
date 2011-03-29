"""
"""
from django.contrib import admin

from zilla.jukebox import models

class SongInlineAdmin(admin.TabularInline):
    """Allow inline editing of songs on the Album admin page."""
    model = models.Song
    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    inlines = [SongInlineAdmin,]


admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Artist)
admin.site.register(models.Song)


