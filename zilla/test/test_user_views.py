"""
"""

from django import test as unittest
from django.test import client

from django.contrib.auth import SESSION_KEY
from django.contrib.auth import models
#from zilla.jukebox import models
#from zilla.jukebox import views


class TestIndex(unittest.TestCase):
    def test_jukebox_list_as_index(self):
        """For now we'll just use the jukebox_list
        as our index page.

        """
        response = self.client.post("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([t.name for t in response.templates],
                         ["jukebox/index.html", "base.html"])
        

class TestLogin(unittest.TestCase):
    """Confirm that a user can login with the correct
    username and password.

    """
    def test_no_credentials(self):
        response = self.client.post("/accounts/login/", {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Your username and password didn't match. Please try again." in response.content)

    def test_invalid_credentials(self):
        response = self.client.post("/accounts/login/",
                                    {"username":"someuser",
                                     "password":"somepass"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Your username and password didn't match. Please try again." in response.content)

    def test_valid_credentials(self):
        models.User.objects.create_user("mike",
                                       "mike@localhost.com",
                                       "mikepass")
        response = self.client.post("/accounts/login/",
                                    {"username":"mike",
                                     "password":"mikepass",
                                     })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"],
                         "http://testserver/accounts/profile/")

    def test_anonymous_account_profile(self):
        """Anonymous in users should be prompted to login
        when attempting to view their account profile.

        """
        self.client.login(username="someuser",
                          password="somepass")
        response = self.client.get("/accounts/profile/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"],
                         "http://testserver/accounts/login/?next=/accounts/profile/")

    def test_account_profile(self):
        """Logged in users should be able to access their
        account profile.

        """
        models.User.objects.create_user("mike",
                                       "mike@localhost.com",
                                       "mikepass")
        self.client.login(username="mike",
                          password="mikepass")
        response = self.client.get("/accounts/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("mike@localhost.com" in response.content,
                        "User e-mail should be in profile page content")

    def test_logout(self):
        """Logged in users should be able to logout.

        """
        u = models.User.objects.create_user("mike",
                                       "mike@localhost.com",
                                       "mikepass")
        self.client.login(username="mike",
                          password="mikepass")
        self.assertEqual(self.client.session[SESSION_KEY], u.id)
        response = self.client.post("/accounts/logout", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not self.client.session.has_key(SESSION_KEY))


class TestResetPassword(unittest.TestCase):
    """Confirm that a user can reset their password
    in the event that they forget.

    """


class TestRegister(unittest.TestCase):
    """Confirm a user can register for a new account.

    """
    def test_register_form(self):
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Username" in response.content)

    def test_register_new_user_valid(self):
        response = self.client.post("/accounts/register/",
                                    {"username":"mike",
                                     "password1":"mikepass",
                                     "password2":"mikepass"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"],
                         "http://testserver/accounts/profile/")
        users = [u for u in models.User.objects.all()]
        self.assertEqual(len(users), 1)
        u = users[0]
        self.assertEqual(u.username, "mike")

    def test_post_register_auto_login(self):
        """Confirm that after registering the user is logged in and redirected.

        """
        response = self.client.post("/accounts/register/",
                                    {"username":"mike",
                                     "password1":"mikepass",
                                     "password2":"mikepass"},
                                    follow=True)

        users = [u for u in models.User.objects.all()]
        self.assertEqual(len(users), 1, "Successful registration must create a user")
        u = users[0]
        self.assertEqual(u.username, "mike")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.has_key(SESSION_KEY),
                        "After registration the user should be logged in.")
        self.assertEqual(self.client.session[SESSION_KEY],
                         u.id)

    def test_register_new_user_invalid(self):
        response = self.client.post("/accounts/register/",
                                    {"username":"mike",
                                     "password1":"mikepass",
                                     "password2":"typopass"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue("The two password fields didn&#39;t match." in response.content)
        
