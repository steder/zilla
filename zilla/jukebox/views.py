#-*- test-case-name: zilla.jukebox.test_views
"""
Create your views here.
"""

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from zilla.jukebox import models


def album_list(request):
    albums = models.Album.objects.all()
    return render_to_response("jukebox/album_list.html",
                              {"albums": albums,
                               "user": request.user},
                              context_instance=RequestContext(request))


def album_detail(request, album_id):
    album = get_object_or_404(models.Album, pk=album_id)
    return render_to_response("jukebox/album_detail.html",
                              {"album": album,
                               "user": request.user},
                              context_instance=RequestContext(request))


def song_detail(request, song_id):
    song = get_object_or_404(models.Song, pk=song_id)

    if request.GET.get("play", False):
        return HttpResponseRedirect(
            "/streaming/song/%s"%(song_id,))

    return render_to_response("jukebox/song_detail.html",
                              {"song": song,
                               "album": song.album,
                               "artist": song.artist,
                               "user": request.user},
                              context_instance=RequestContext(request))
    
