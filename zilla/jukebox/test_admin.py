from django.contrib.auth import models
from django import test as unittest
from django.test import client


class TestAdminViews(unittest.TestCase):
    """Confirm that the admin views exist for specific models.
    """

    client_class = client.Client

    def test_album(self):
        response = self.client.get("/admin/jukebox/album/")
        self.assertEqual(response.status_code, 200)

    def test_artist(self):
        response = self.client.get("/admin/jukebox/artist/")
        self.assertEqual(response.status_code, 200)

    def test_jukebox(self):
        response = self.client.get("/admin/jukebox/jukebox/")
        self.assertEqual(response.status_code, 200)

    def test_plural_jukebox(self):
        models.User.objects.create_superuser("mike",
                                       "mike@localhost.com",
                                       "mikepass")
        self.client.login(username="mike",
                          password="mikepass")

        response = self.client.get("/admin/jukebox/jukebox/")
        self.assertTrue("jukeboxes" in response.content, "The correct plural for jukebox is jukeboxes")

    def test_song(self):
        response = self.client.get("/admin/jukebox/song/")
        self.assertEqual(response.status_code, 200)
        

