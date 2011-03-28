#-*- test-case-name: zilla.jukebox.test_views
"""
Create your views here.
"""

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from zilla.jukebox import models

def index(request): #TODO: change to jukebox_list
    boxes = models.Jukebox.objects.all()
    return render_to_response("jukebox/index.html", {"jukeboxes":boxes, "user":request.user})


def jukebox_detail(request, jukebox_id):
    jukebox_id = int(jukebox_id)
    try:
        jukebox = models.Jukebox.objects.get(id=jukebox_id)
    except models.Jukebox.DoesNotExist:
        raise Http404
    return render_to_response("jukebox/jukebox_detail.html",
                              {"jukebox": jukebox,
                               "user": request.user})


def album_detail(request, album_id):
    album = get_object_or_404(models.Album, pk=album_id)
    return render_to_response("jukebox/album_detail.html",
                              {"album": album,
                               "user": request.user})


def song_detail(request, song_id):
    song = get_object_or_404(models.Song, pk=song_id)

    if request.GET.get("play", False):
        return HttpResponseRedirect(
            "/streaming/song/%s"%(song_id,))

    return render_to_response("jukebox/song_detail.html",
                              {"song": song,
                               "user": request.user})
    
