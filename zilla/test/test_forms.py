"""
"""

from django import test as unittest

from zilla import forms


class TestUserCreationForm(unittest.TestCase):
    def test_register(self):
        f = forms.UserCreationForm({"username":"u1",
                                    "email":"u1@example.com",
                                    "password1":"pass",
                                    "password2":"pass"})
        f.is_valid()
        user = f.save()
        self.assertEqual(user.username, "u1")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)


