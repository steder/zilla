"""
"""


from django import test as unittest

from zilla.jukebox import forms


class TestSearchForm(unittest.TestCase):
    def test_search_invalid(self):
        form = forms.SearchForm()
        self.assertEqual(form.is_bound, False)
        self.assertEqual(form.is_valid(), False)

    def test_search_valid(self):
        form = forms.SearchForm({"keywords":"hello",
                                 })
        self.assertEqual(form.is_bound, True)
        self.assertEqual(form.is_valid(), True)

    def test_search_keywords_field(self):
        form = forms.SearchForm({"keywords":"hello",
                                 "category":"album"})
        self.assertEqual(form.is_bound, True)
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.data["keywords"], "hello")

    def test_search_keywords_search_category(self):
        form = forms.SearchForm({"keywords":"hello",
                                 "category":"title"})
        self.assertEqual(form.is_bound, True)
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.data["category"], "title")
