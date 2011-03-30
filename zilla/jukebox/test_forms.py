"""
"""


from django import test as unittest

from zilla.jukebox import forms


class TestSearchForm(unittest.TestCase):
    def test_search(self):
        form = forms.SearchForm()
        self.assertEqual(form.is_valid(), False)

    def test_search_valid(self):
        form = forms.SearchForm({"keywords":"hello"})
        self.assertEqual(form.is_valid(), True)
        


