"""Forms for the Jukebox application.

SearchForm

"""


from django.contrib.auth.models import User
#from django.contrib.auth import authenticate
#from django.contrib.auth.tokens import default_token_generator
#from django.contrib.sites.models import get_current_site
#from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
#from django.utils.http import int_to_base36

from zilla.jukebox import models

CATEGORIES = (
    ("album","Album"),
    ("artist","Artist"),
    ("title","Title"),
)

class SearchForm(forms.Form):
    """
    A form that builds a search query.
    """
    keywords = forms.CharField(label=_("Keywords"), max_length=255, required=False)
    category = forms.ChoiceField(choices=CATEGORIES, initial=3, required=False)

