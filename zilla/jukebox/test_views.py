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

    def test_jukebox_app(self):
        response = self.client.get("/jukebox/")
        self.assertEqual(response.status_code, 200)
    

class TestJukeboxIndex(unittest.TestCase):
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
        
