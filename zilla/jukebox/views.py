#-*- test-case-name: zilla.jukebox.test_views
"""
Create your views here.
"""
from django.http import HttpResponse
from django.shortcuts import render_to_response

from zilla.jukebox import models

def index(request):
    boxes = models.Jukebox.objects.all()
    return render_to_response("jukebox/index.html", {"jukeboxes":boxes, "user":request.user})
