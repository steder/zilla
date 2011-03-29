"""
"""

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from zilla import forms

@login_required
def profile(request):
    """View the users profile."""
    c = {"user":request.user}
    return render_to_response("registration/profile.html", c)

def register(request):
    """Allow anonymous users to create accounts."""
    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(username=request.POST["username"],
                                     password=request.POST["password1"])
            auth.login(request, user)
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = forms.UserCreationForm()
    c = {"form":form}
    return render_to_response("registration/register.html", c,
                              context_instance=RequestContext(request))

