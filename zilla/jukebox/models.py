"""Jukebox models

Album - Represents a collection of songs owned by an Artist.
Artist - Represents a musician or band.
Jukebox - Represents a collection of songs owned by a Jukebox Owner.
Song - Represents a song owned by an Artist.

"""

from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey("Artist", null=True, blank=True,
                               related_name="album_set")

    @property
    def songs(self):
        for song in self.song_set.all():
            yield song

    @property
    def played(self):
        played = 0
        for song in self.songs:
            played += song.played 
        return played

    def __unicode__(self):
        if self.artist:
            return "%s by %s"%(self.title, self.artist)
        return "%s"%(self.title,)

    @models.permalink
    def get_absolute_url(self):
        return ('zilla.jukebox.views.album_detail', (), {"album_id":self.id})


class Artist(models.Model):
    name = models.CharField(max_length=255)

    @property
    def albums(self):
        for album in self.album_set.all():
            yield album

    @property
    def songs(self):
        for song in self.song_set.all():
            yield song

    @property
    def played(self):
        """Determine how many times this Artists songs have been played.

        Story: As a listener, I should be able to see what is the most
        commonly played artist.
        """
        played = 0
        for song in self.songs:
            played += song.played
        return played

    def __unicode__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, blank=True, null=True,
                               related_name="song_set")
    album = models.ForeignKey(Album, blank=True, null=True,
                              related_name="song_set")
    genre = models.CharField(max_length=255, blank=True, default="")
    played = models.BigIntegerField(default=0,
                                    help_text=("A listener should be able to "
                                               "see what is the most commonly "
                                               "played song.")
                                    )
    playable = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s"%(self.title,)

    @models.permalink
    def get_absolute_url(self):
        return ('zilla.jukebox.views.song_detail', (), {"song_id":self.id})
