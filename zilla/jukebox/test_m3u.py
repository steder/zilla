from django import test as unittest
from nose import SkipTest

#from zilla import m3u


class TestM3U(unittest.TestCase):
    def test_jukebox_m3u(self):
        """The streaming urls for all songs in the jukebox should be included in the m3u generated from accessing this url."""
        raise SkipTest("Let's do this later: after search is working")
        response = self.client.get("/jukebox/m3u")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "/streaming/song/1\n/streaming/song/2")
