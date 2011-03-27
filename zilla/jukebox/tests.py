"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from zilla.jukebox import models


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class TestAlbum(TestCase):
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


class TestArtist(TestCase):
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


class TestJukebox(TestCase):
    def setUp(self):
        self.jukebox = models.Jukebox(name="Jukebox Prime")

    def test_name(self):
        self.assertEqual(self.jukebox.name, "Jukebox Prime")

    def test_albums(self):
        self.jukebox.save()
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        album.save()
        self.jukebox.add_album(album)
        self.assertEqual(len(self.jukebox.albums.all()), 1)

    def _setup_album_with_songs(self):
        self.jukebox.save()
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        album.save()
        song = models.Song(title="Bein' Green", album=album)
        song.save()
        self.jukebox.add_album(album)

    def test_adding_album_with_songs(self):
        """Adding an album should also add song records to the jukebox.
        """
        self._setup_album_with_songs()
        self.assertEqual(len(self.jukebox.songs.all()), 1)

    def test_adding_album_with_songs_playability(self):
        """By default all songs should be playable."""
        self._setup_album_with_songs()
        self.assertEqual(len(self.jukebox.songs.all()), 1)
        self.assertEqual(all(song.is_playable(self.jukebox) for song in self.jukebox.songs.all()), True)

    def test_adding_album_with_non_playable_songs(self):
        self._setup_album_with_songs()
        for song in self.jukebox.songs.all():
            song.set_playable(self.jukebox, False)
        self.assertEqual([song.is_playable(self.jukebox) for song in self.jukebox.songs.all()], [True,])   

    def test_remove_album(self):
        self._setup_album_with_songs()
        self.assertEqual(len(self.jukebox.albums.all()), 1)
        self.assertEqual(len(self.jukebox.songs.all()), 1)
        for album in self.jukebox.albums.all():
            self.jukebox.remove_album(album)
        self.assertEqual(len(self.jukebox.albums.all()), 0)
        self.assertEqual(len(self.jukebox.songs.all()), 0)

        
class TestSong(TestCase):
    def setUp(self):
        artist = models.Artist(name="Kermit the Frog")
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites",
                             artist=artist)
        self.s = models.Song(title="Bein' Green",
                             artist=artist,
                             album=album,
                             genre="Children's Music")

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


    
