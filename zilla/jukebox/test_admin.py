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

    def test_song(self):
        response = self.client.get("/admin/jukebox/song/")
        self.assertEqual(response.status_code, 200)
        

