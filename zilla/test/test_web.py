"""test_web.py

Tests for the Zilla t.w.Resources
"""
#from datetime import datetime

import mock

from nose import SkipTest
from twisted.trial import unittest
from twisted.web import resource
from twisted.web import static
from twisted.web import server
from twisted.web.test.test_web import DummyRequest
#from twisted.web._auth.wrapper import HTTPAuthSessionWrapper

from zilla import web


class TestRootGetChild(unittest.TestCase):
    """getChild just does dynamic lookup of child
    resources.

    """

    def setUp(self):
        testServer = mock.Mock()
        self.r = web.Root(testServer)

    def test_getRoot(self):
        """The root url should be handed off to wsgiResource
        """
        request = mock.Mock()
        request.prepath.pop.return_value = ""
        r = self.r.getChild("", request)
        self.assertEqual(r, web.django)
        request.postpath.insert.assert_called_with(0, "")

    def test_anythingElse(self):
        """Everything else is handed off to the wsgiResource

        """
        request = mock.Mock()
        request.prepath.pop.return_value = "test"
        r = self.r.getChild("test/random.html", request)
        self.assertTrue(r, web.django)
        request.postpath.insert.assert_called_with(0, "test")

    def test_streaming(self):
        """File Streaming is handled by twisted."""
        request = mock.Mock()
        request.prepath.pop.return_value = "streaming"
        r = self.r.getChild("streaming/song/1", request)
        self.assertTrue(r, web.Streaming)


class TestRoot_getChildWithDefault(unittest.TestCase):
    """getChildWithDefault is the the call that takes into
    account static resources and then calls getChild to
    check for dynamic resources.

    """
    def setUp(self):
        testServer = mock.Mock()
        self.r = web.Root(testServer)

    def test_getRoot(self):
        """The root url should be handed off to wsgiResource
        """
        request = mock.Mock()
        request.prepath.pop.return_value = ""
        r = self.r.getChildWithDefault("", request)
        self.assertEqual(r, web.django)
        request.postpath.insert.assert_called_with(0, "")

    def test_anythingElse(self):
        """Everything else is handed off to the wsgiResource

        """
        request = mock.Mock()
        request.prepath.pop.return_value = "test"
        r = self.r.getChildWithDefault("test/random.html", request)
        self.assertEqual(r, web.django)
        request.postpath.insert.assert_called_with(0, "test")

    def test_getStatic(self):
        """Urls including '/static/' should be served by
        the static directory web resource

        """
        r = self.r.getChildWithDefault("static", None)
        self.assertEqual(True, isinstance(r, static.File))

    def test_getFavicon(self):
        """The root '/favicon.ico' should be accessible

        """
        r = self.r.getChildWithDefault("favicon.ico", None)
        self.assertEqual(True, isinstance(r, static.File))


class TestStreaming(unittest.TestCase):
    def setUp(self):
        self.r = web.Streaming()

    def test_getChild_song(self):
        """The next url segment will be the streaming data type.

        For now this is only "song".  Everything else
        results in a 404.
        
        """
        request = mock.Mock()
        r = self.r.getChild("song", request)
        self.assertTrue(isinstance(r, web.Songs))

    def test_getChild_anything_but_song(self):
        """The next url segment will be the streaming data type.

        For now this is only "song".  Everything else
        results in a 404.
        
        """
        request = mock.Mock()
        r = self.r.getChild("video", request)
        self.assertTrue(isinstance(r, resource.NoResource))


class TestSongs(unittest.TestCase):
    def setUp(self):
        self.r = web.Songs()

    def test_getChild_root(self):
        request = mock.Mock()
        r = self.r.getChild("", request)
        self.assertTrue(isinstance(r, resource.NoResource))
        
    def test_getChild_float(self):
        request = mock.Mock()
        r = self.r.getChild("1.3", request)
        self.assertTrue(isinstance(r, resource.NoResource))
        
    def test_getChild_text(self):
        request = mock.Mock()
        r = self.r.getChild("Bein' Green", request)
        self.assertTrue(isinstance(r, resource.NoResource))

    def test_getChild_song_id(self):
        request = mock.Mock()
        r = self.r.getChild("1", request)
        self.assertTrue(isinstance(r, web.Song), "Songs.getChild with a valid song_id should return a Song resource")


class TestSong(unittest.TestCase):
    def _assert_song_does_not_exist(self, ignored, request):
        self.assertEqual(request.responseCode, 404)

    def test_song_id_does_not_exist(self):
        raise SkipTest("Twisted using deferToThread seems to break the test db connection that django establishes.  However, with the real django db connection this works fine...")
        r = web.Song(1)
        request = DummyRequest([""])
        d = request.notifyFinish()
        d.addCallback(self._assert_song_does_not_exist, request)
        result = r.render_GET(request)
        self.assertEqual(result, server.NOT_DONE_YET)
        return d
        
    def _create_song(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""insert into jukebox_song (id, title, genre, played) values (1, 'My Song', 'My Genre', 0)""")
        self.assertEqual(cursor.rowcount, 1)
        
    def test_song_id_does_exist(self):
        raise SkipTest("Twisted using deferToThread seems to break the test db connection that django establishes.  However, with the real django db connection this works fine...")

        self._create_song()
        r = web.Song(1)
        request = mock.Mock()
        result = r.render_GET(request)
        self.assertEqual(result, "Song 1 playcount => 0")
        
