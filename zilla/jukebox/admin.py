"""
"""
from django.contrib import admin

from zilla.jukebox import models

admin.site.register(models.Album)
admin.site.register(models.Artist)
admin.site.register(models.Song)
