"""Tests for zilla.jukebox.views
"""

import BeautifulSoup as bs
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
        self.assertTrue("I'm sorry, Zilla can't find /random/garbage/page..." in response.content,
                         "404 page should include an error message about the missing page.")

    def test_jukebox_index(self):
        response = self.client.get("/jukebox/")
        self.assertEqual(response.status_code, 200)
    

class TestAlbumListView(unittest.TestCase):
    """Check how a the Jukebox Index view works
    a specific request (generated with RequestFactory)

    """
    client_class = client.Client

    def test_list_without_albums(self):
        response = self.client.get("/jukebox/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jukebox" in response.content, "index page should refer to Jukebox")
        self.assertEqual(len(response.context["albums"]), 0)

    def test_list_with_album(self):
        a1 = models.Album(title="Album 1")
        a1.save()
        response = self.client.get("/jukebox/")
        self.assertEqual(len(response.context["albums"]), 1)
        soup = bs.BeautifulSoup(response.content)
        anchors = soup.findAll("a", attrs={"class":"album"})
        self.assertEqual(anchors[0].text, u"Album 1")
        self.assertEqual(anchors[0]["href"], u"/album/%s"%(a1.id,))

    def test_list_with_albums(self):
        n_albums = 3
        for x in xrange(n_albums):
            j = models.Album(title="Album %s"%(x,))
            j.save()
        response = self.client.get("/jukebox/")
        self.assertEqual(len(response.context["albums"]),
                         n_albums)
        
    def test_search_link(self):
        response = self.client.get("/jukebox/")
        self.assertTrue("""<a href="/songs/">Search</a>"""
                        in response.content, "A link to the search page should be on this page")

    def test_show_albums(self):
        for x in xrange(1, 3):
            a = models.Album(title="Album %s"%(x,))
            a.save()
        response = self.client.get("/jukebox/")
        soup = bs.BeautifulSoup(response.content)
        anchors = soup.findAll("a", attrs={"class":"album"})
        self.assertEqual(anchors[0].text, "Album 1")
        self.assertEqual(anchors[0]["href"], "/album/%s"%(1,))
        self.assertEqual(anchors[1].text, "Album 2")
        self.assertEqual(anchors[1]["href"], "/album/%s"%(2,))


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

        soup = bs.BeautifulSoup(response.content)
        anchors = soup.findAll("a", attrs={"class":"song"})
        self.assertEqual(anchors[0].text, u"Song #1")
        self.assertEqual(anchors[0]["href"], u"/song/%s"%(song.id))

    def test_show_album_with_songs(self):
        album = models.Album(title="My First Album")
        album.save()
        for x in xrange(1, 4):
            song = models.Song(title="Song #%s"%(x,))
            song.album = album
            song.save()
        response = self.client.get("/album/%s"%(album.id,))
        self.assertEqual(response.status_code, 200)

        soup = bs.BeautifulSoup(response.content)
        anchors = soup.findAll("a", attrs={"class": "song"})
        # these can come back in any order depending on the database
        # backend:
        text = set([a.text for a in anchors])
        self.assertEqual(text, set([u"Song #1", u"Song #2", u"Song #3"]))
        hrefs = set([a["href"] for a in anchors])
        self.assertEqual(hrefs, set([u"/song/1", u"/song/2", u"/song/3"]))


class TestSongDetailView(unittest.TestCase):
    def test_show_missing_song(self):
        response = self.client.get("/song/7")
        self.assertEqual(response.status_code, 404)
    
    def test_show_song(self):
        song = models.Song(title="Song #1")
        song.save()
        response = self.client.get("/song/%s"%(song.id,))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Song #1" in response.content,
                        "'Song #1' should appear in the album detail view.")

    def test_show_song_play_link(self):
        song = models.Song(title="Song #1")
        song.save()
        response = self.client.get("/song/%s"%(song.id,))

        soup = bs.BeautifulSoup(response.content)
        anchors = soup.findAll("a", attrs={"class":"play"})
        self.assertEqual(anchors[0].text, u"Play")
        self.assertEqual(anchors[0]["href"], u"/streaming/song/%s"%(song.id))


class TestSearchView(unittest.TestCase):
    def test_search(self):
        response = self.client.get("/songs/")
        self.assertEqual(response.status_code, 200)
        
    def test_search_invaild(self):
        song = models.Song(title="Bein' Green")
        song.save()
        response = self.client.get("/songs/?keywords=green")
        self.assertEqual(response.context["songs"], [])

    def test_search_valid_title(self):
        song = models.Song(title="Bein' Green")
        song.save()
        response = self.client.get("/songs/?keywords=green&category=title")
        self.assertEqual([song.title for song in response.context["songs"]],
                         [song.title])
        
    def test_search_valid_album(self):
        album = models.Album(title="Sesame Street: Platinum All-Time Favorites")
        album.save()
        song = models.Song(title="Bein' Green", album=album)
        song.save()
        response = self.client.get("/songs/?keywords=sesame&category=album")
        self.assertEqual([song.title for song in response.context["songs"]],
                         [song.title])

    def test_search_valid_artist(self):
        artist = models.Artist(name="Kermit the Frog")
        artist.save()
        song = models.Song(title="Bein' Green", artist=artist)
        song.save()
        response = self.client.get("/songs/?keywords=frog&category=artist")
        self.assertEqual([song.title for song in response.context["songs"]],
                         [song.title])

        
