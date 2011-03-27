"""Tests for zilla.jukebox.views
"""

from django import test as unittest
from django.test import client

from zilla.jukebox import models
from zilla.jukebox import views


class TestJukeboxViews(unittest.TestCase):
    """Check to see if views are defined, if redirects
    occur properly, and that routes work as expected.

    """
    client_class = client.Client

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_404_view(self):
        response = self.client.get("/random/garbage/page")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("I'm sorry, we don't know where to find /random/garbage/page..." in response.content,
                         "404 page should include an error message about the missing page.")

    def test_jukebox_index(self):
        response = self.client.get("/jukebox/")
        self.assertEqual(response.status_code, 200)
    

class TestJukeboxListView(unittest.TestCase):
    """Check how a the JukeboxIndex view works
    a specific request (generated with RequestFactory)

    """
    client_class = client.Client
    #fixtures = ["jukebox_index.json"]

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_index_without_jukeboxes(self):
        response = self.client.get("/jukebox/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jukeboxes" in response.content, "index page should refer to Jukeboxes")
        self.assertEqual(len(response.context["jukeboxes"]), 0)

    def test_index_with_jukebox(self):
        j1 = models.Jukebox(name="Jukebox 1")
        j1.save()
        response = self.client.get("/jukebox/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jukeboxes" in response.content, "index page should refer to Jukeboxes")
        self.assertEqual(len(response.context["jukeboxes"]), 1)
        self.assertTrue("Jukebox 1" in response.content, "index page should contain a reference to Jukebox 1")

    def test_index_with_jukeboxes(self):
        n_jukeboxes = 3
        for x in xrange(n_jukeboxes):
            j = models.Jukebox(name="Jukebox %s"%(x,))
            j.save()
        response = self.client.get("/jukebox/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jukeboxes" in response.content, "index page should refer to Jukeboxes")
        self.assertEqual(len(response.context["jukeboxes"]),
                         n_jukeboxes)
        

class TestJukeboxDetailView(unittest.TestCase):
    """A jukebox specific page should list all the albums
    within a given jukebox.

    """
    def test_show_missing_jukebox(self):
        response = self.client.get("/jukebox/7")
        self.assertEqual(response.status_code, 404)

    def test_show_jukebox(self):
        j1 = models.Jukebox(name="Jukebox 1")
        j1.save()
        response = self.client.get("/jukebox/%s"%(j1.id,))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jukebox 1" in response.content,
                        "The jukebox page should list the jukebox name.")
        
    def test_show_album(self):
        album = models.Album(title="Album 1")
        album.save()
        j1 = models.Jukebox(name="Jukebox 1")
        j1.save()
        j1.add_album(album)

        response = self.client.get("/jukebox/%s"%(j1.id,))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jukebox 1" in response.content,
                        "The jukebox page should list the jukebox name.")
        self.assertTrue("Album 1" in response.content,
                        "The jukebox page should list 'Album 1'.")
        
    def test_show_albums(self):
        j1 = models.Jukebox(name="Jukebox 1")
        j1.save()
        for x in xrange(1, 3):
            a = models.Album(title="Album %s"%(x,))
            a.save()
            j1.add_album(a)

        response = self.client.get("/jukebox/%s"%(j1.id,))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jukebox 1" in response.content,
                        "The jukebox page should list the jukebox name.")
        self.assertTrue("Album 1" in response.content,
                        "The jukebox page should list 'Album 1'.")
        self.assertTrue("Album 2" in response.content,
                        "The jukebox page should list 'Album 2'.")


class TestAlbumDetailView(unittest.TestCase):
    def test_show_missing_album(self):
        response = self.client.get("/album/7")
        self.assertEqual(response.status_code, 404)
    
    def test_show_album(self):
        album = models.Album(title="My First Album")
        album.save()
        response = self.client.get("/album/%s"%(album.id,))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("My First Album" in response.content,
                        "'My First Album' should appear in the album detail view.")

    def test_show_album_with_song(self):
        album = models.Album(title="My First Album")
        album.save()
        song = models.Song(title="Song #1")
        song.album = album
        song.save()

        response = self.client.get("/album/%s"%(album.id,))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Song #1" in response.content,
                        "'Song #1' should appear in the album detail view.")

    def test_show_album_with_songs(self):
        album = models.Album(title="My First Album")
        album.save()
        for x in xrange(1, 4):
            song = models.Song(title="Song #%s"%(x,))
            song.album = album
            song.save()
        response = self.client.get("/album/%s"%(album.id,))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Song #1" in response.content,
                        "'Song #1' should appear in the album detail view.")
        self.assertTrue("Song #2" in response.content,
                        "'Song #2' should appear in the album detail view.")
        self.assertTrue("Song #3" in response.content,
                        "'Song #3' should appear in the album detail view.")
