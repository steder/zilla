#-*- test-case-name: zilla.jukebox.test_views
"""
Create your views here.
"""

from django.db.models import Count, Sum
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from zilla.jukebox import forms
from zilla.jukebox import models


def album_list(request):
    albums = models.Album.objects.all().order_by(
        "title", "artist__name").annotate(
        Sum("song_set__played")).annotate(
            Count("song_set")).values("id", "title",
                     "artist__name", "song_set__played__sum",
                                      "song_set__count")
    return render_to_response("jukebox/album_list.html",
                              {"albums": albums,
                               "user": request.user},
                              context_instance=RequestContext(request))


def album_detail(request, album_id):
    try:
        album = models.Album.objects.select_related("artist").get(id=album_id)
    except models.Album.DoesNotExist:
        raise Http404
    songs = models.Song.objects.filter(album=album).values("id", "title",
                                                           "artist__name",
                                                           "played",
                                                           "playable")
    return render_to_response("jukebox/album_detail.html",
                              {"album": album,
                               "songs": songs,
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
    

def search(request):
    form = forms.SearchForm(request.GET)
    form.initial = request.GET
    songs = []

    if form.is_valid():
        keywords = form.cleaned_data["keywords"]
        category = form.cleaned_data["category"]

        if category == "album":
            songs = models.Song.objects.filter(
                album__title__iregex=keywords).all()
        elif category == "artist":
            songs = models.Song.objects.filter(
                artist__name__iregex=keywords).all()
        elif category == "title":
            songs = models.Song.objects.filter(title__iregex=keywords).all()

    return render_to_response("jukebox/search.html",
                              {"form":form,
                               "songs":songs},
                              context_instance=RequestContext(request))
