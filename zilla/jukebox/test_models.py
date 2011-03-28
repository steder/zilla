"""Tests for zilla.jukebox.models
"""

from django import test as unittest

from zilla.jukebox import models


class TestAlbum(unittest.TestCase):
    def test_title(self):
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        self.assertEqual(album.title,
                         "Sesame Street: Platinum All-Time Favorites")

    def test_songs(self):
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        song = models.Song(title="Bein' Green", album=album)
        album.song_set = [song]
        titles = [song.title for song  in album.songs]
        self.assertEqual(titles, ["Bein' Green",])

    def test_unplayed(self):
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        song = models.Song(title="Bein' Green")
        song.album = album
        album.song_set = [song]
        self.assertEqual(album.played, 0)

    def test_played(self):
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        song = models.Song(title="Bein' Green")
        song.album = album
        song.played = 373
        album.song_set = [song]
        self.assertEqual(album.played, 373)
        
    def test_played_multiple_songs(self):
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        song = models.Song(title="Bein' Green")
        song.album = album
        song.played = 373
        song2 = models.Song(title="Bein' Green")
        song2.album = album
        song2.played = 1
        album.song_set = [song, song2]
        self.assertEqual(album.played, 374)

    def test_unicode_without_artist(self):
        album = models.Album(title=u"Sesame Street")
        self.assertEqual(unicode(album), u"Sesame Street")

    def test_unicode_with_artist(self):
        artist = models.Artist(name="Kermit")
        album = models.Album(title=u"Sesame Street", artist=artist)
        self.assertEqual(unicode(album), u"Sesame Street by Kermit")
        

class TestArtist(unittest.TestCase):
    def test_name(self):
        artist = models.Artist(name="Kermit the Frog")
        self.assertEqual(artist.name, "Kermit the Frog")

    def test_albums(self):
        """An artist should have a reference to all their albums."""
        artist = models.Artist(name="Kermit the Frog")
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        album.artist = artist
        artist.album_set = [album]
        self.assertEqual([a.title for a in artist.albums],
                         ["Sesame Street: Platinum All-Time Favorites",])

    def test_songs(self):
        """An artist should have a reference to all their songs."""
        artist = models.Artist(name="Kermit the Frog")
        song = models.Song(title="Bein' Green")
        song.artist = artist
        artist.song_set = [song]
        self.assertEqual([a.title for a in artist.songs],
                         ["Bein' Green",])

    def test_unplayed(self):
        artist = models.Artist(name="Kermit the Frog")
        song = models.Song(title="Bein' Green")
        song.artist = artist
        artist.song_set = [song]
        self.assertEqual(artist.played, 0)

    def test_played(self):
        artist = models.Artist(name="Kermit the Frog")
        song = models.Song(title="Bein' Green")
        song.artist = artist
        song.played = 373
        artist.song_set = [song]
        self.assertEqual(artist.played, 373)
        
    def test_played_multiple_songs(self):
        artist = models.Artist(name="Kermit the Frog")
        song = models.Song(title="Bein' Green")
        song.artist = artist
        song.played = 373
        song2 = models.Song(title="Bein' Green")
        song2.artist = artist
        song2.played = 1
        artist.song_set = [song, song2]
        self.assertEqual(artist.played, 374)

    def test_unicode(self):
        artist = models.Artist(name="Kermit the Frog")
        self.assertEqual(str(artist), "Kermit the Frog")


class TestSong(unittest.TestCase):
    def setUp(self):
        artist = models.Artist(name="Kermit the Frog")
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites",
                             artist=artist)
        self.s = models.Song(title="Bein' Green",
                             artist=artist,
                             album=album,
                             genre="Children's Music")

    def test_unicode(self):
        self.assertEqual(str(self.s), "Bein' Green")

    def test_title(self):
        self.assertEqual(self.s.title, "Bein' Green")

    def test_artist(self):
        self.assertEqual(self.s.artist.name, "Kermit the Frog")

    def test_album(self):
        self.assertEqual(self.s.album.title, "Sesame Street: Platinum All-Time Favorites")

    def test_genre(self):
        self.assertEqual(self.s.genre, "Children's Music")

    def test_played(self):
        """A newly created song should have a played count of 0"""
        self.assertEqual(self.s.played, 0)

    def test_playable(self):
        """Newly created songs have a default playabilty of 'True'.
        """
        self.assertEqual(self.s.playable, True)
    
