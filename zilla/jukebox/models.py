"""Jukebox models

Album - Represents a collection of songs owned by an Artist.
Artist - Represents a musician or band.
Jukebox - Represents a collection of songs owned by a Jukebox Owner.
Song - Represents a song owned by an Artist.

"""

from django.db import models

class Album(models.Model):
    title = models.TextField()
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


class Artist(models.Model):
    name = models.TextField()

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


class Jukebox(models.Model):
    class Meta:
        verbose_name_plural = "jukeboxes"

    name = models.TextField()
    albums = models.ManyToManyField(Album, related_name="+")
    songs = models.ManyToManyField("Song", related_name="+", through="JukeboxSong")

    def __unicode__(self):
        return self.name

    def add_album(self, album):
        """Add an album to this jukebox.

        As the jukebox owner, I should be able to add or remove an album
        in the jukebox.

        """
        self.albums.add(album)
        for song in album.songs:
            #self.songs.add(song)
            js = JukeboxSong(jukebox=self,
                        song=song)
            js.save()

    def remove_album(self, album):
        """Remove an album from this jukebox.

        As the jukebox owner, I should be able to add or remove an album
        in the jukebox.

        """
        self.albums.remove(album)
        for song in album.songs:
            js = song.get_jukeboxsong(self)
            if js:
                js.delete()


class JukeboxSong(models.Model):
    jukebox = models.ForeignKey(Jukebox, related_name="jukeboxsong_set")
    song = models.ForeignKey("Song", related_name="jukeboxsong_set")
    playable = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s in %s"%(self.song,
                           self.jukebox)
    

class Song(models.Model):
    title = models.TextField()
    artist = models.ForeignKey(Artist, blank=True, null=True,
                               related_name="song_set")
    album = models.ForeignKey(Album, blank=True, null=True,
                              related_name="song_set")
    genre = models.TextField(blank=True, default="")
    played = models.BigIntegerField(default=0,
                                    help_text=("A listener should be able to"
                                               "see what is the most commonly"
                                               "played song.")
                                    )

    def played_today(self):
        """I think a more interesting played number
        would allow you to see how much this song is
        being played today vs lifetime plays.  Other time
        intervals (weeks, months, years) etc could be useful
        but in the shortterm being able to differentiate
        between "popular" and "popular today" could be a
        nice addition when we get to the story about:

        "listener can learn what artist, album, song
        is most often played."

        Basically:  we create 2 bins for played
        bin 1: daily
        bin 2: lifetime

        Given the current day matches the last_played_date
        When increment the play count
        Then we increment the daily count.

        Given the current day is greater than the last_played_date
        When we increment the play count
        Then we:
          played_total += played_today
          played_today = 0
          set the last_played_date = current_date

        We calculate played as:
          played = played_today + played_total

        NOTE: another way of doing this that may be more
        powerful would be to store a song_stat record daily, weekly, monthly, whatever.  That song_stat record would allow you to keep
        track of song plays on a daily basis (or whatever interval)
        and retrieve historical data later so instead of just answering questions like what was the most popular song today you could
        make more granular queries like what was the most popular song in the last 3 days.  Or what were the most popular songs 3 weeks ago.  (select plays from song_stats where stat_date < 'today' and stat_date > '3 days ago') or (select plays from song_stats where stat_date < '3 weeks ago' and stat_date > '4 weeks ago')
          
        """
        raise NotImplemented
        
    def played_total(self):
        """
        """
        raise NotImplemented

    def __unicode__(self):
        return "%s"%(self.title,)

    def get_jukeboxsong(self, jukebox):
        js = None
        jukeboxsongs = self.jukeboxsong_set.filter(jukebox=jukebox)
        if jukeboxsongs:
            js = jukeboxsongs[0]
        return js

    def set_playable(self, jukebox, playable):
        js = self.get_jukeboxsong(jukebox)
        js.playable = playable

    def is_playable(self, jukebox):
        """Determine whether this song is playable within the context jukebox.

        On a per jukebox basis a JukeboxOwner is able to refer to song
        as playable or non-playable.  This is specific to just that users
        jukebox, not the song so that while a song may not be playable
        in "Bob's Country Jukebox" the same song could be playable in "Bob's
        Western Jukebox" 

        """
        playable = True
        jukeboxsong = self.get_jukeboxsong(jukebox)
        if jukeboxsong:
            playable = jukeboxsong.playable
        return playable
