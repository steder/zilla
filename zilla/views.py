"""
"""

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from zilla import forms

@login_required
def profile(request):
    """View the users profile."""
    return HttpResponse("Hello World " + request.user.email)

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
    return render_to_response("registration/register.html",
                              {"form":form})

