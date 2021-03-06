#-*- test-case-name: zilla.test.test_web -*-
import os

from twisted.internet import defer
from twisted.internet import threads
from twisted.internet import reactor
from twisted.web import http, resource, server, static
from twisted.web import wsgi

#from txtemplate import templates
from zilla import settings
from zilla import utils
from zilla import whiskey
from zilla.jukebox import models


staticDirectory = static.File(
    settings.STATIC_ROOT
)


django = wsgi.WSGIResource(reactor, reactor.getThreadPool(),
                           whiskey.application)


class Song(resource.Resource):
    isLeaf = True

    def __init__(self, song_id):
        resource.Resource.__init__(self)
        self.song_id = str(song_id)
        
    def _updateSongPlayed(self, request):
        try:
            from django.db import connections
            connections["default"]._dirty = False
            song = models.Song.objects.get(id=int(self.song_id))
            if song.playable:
                song.played += 1
                song.save()
            return song.id, song.played, song.playable
        except models.Song.DoesNotExist:
            return None
            
    def _cbPlayed(self, result, request):
        if result:
            song_id, played, song_playable = result
            if song_playable:
                request.setResponseCode(200)
                request.write("Song %s playcount => %s"%(song_id, played))
            else:
                request.setResponseCode(403)
                request.write("Access Denied: Song %s owner has marked this song as not playable."%(song_id,))
            request.write("\n")            
            request.finish()
        else:
            request.setResponseCode(404)
            request.write("Missing song: %s"%(self.song_id,))
            request.write("\n")
            request.finish()

    def _ebPlayed(self, error, request):
        request.setResponseCode(500)
        request.write("Error: %s"%(error,))
        request.write("\n")
        request.finish()

    def render_GET(self, request):
        d = threads.deferToThread(self._updateSongPlayed, request)
        d.addCallback(self._cbPlayed, request)
        d.addErrback(self._ebPlayed, request)
        return server.NOT_DONE_YET


class Songs(resource.Resource):
    """Resource representing the all songs"""
    @utils.logMethodTime
    def getChild(self, path, request):
        song_id = None
        try:
            song_id = int(path)
        except ValueError:
            pass
        if song_id:
            return Song(song_id)
        else:
            return resource.Resource.getChild(self, path, request)

    
class Streaming(resource.Resource):
    """Handles file streaming."""

    @utils.logMethodTime
    def getChild(self, path, request):
        if path == "song":
            return Songs()
        else:
            return resource.Resource.getChild(self, path, request)


class Root(resource.Resource):
    @utils.logMethodTime
    def __init__(self, server):
        resource.Resource.__init__(self)
        self.server = server
        self.putChild('static', staticDirectory)
        self.putChild("favicon.ico", static.File(
                settings.FAVICON
                )
        )

    def render_GET(self, request):
        return """<html>
<head><title>Hello World</title></head>
<body><h1>Hello World!</h1>
</body>
</html>"""

    @utils.logMethodTime
    def getChild(self, path, request):
        if path == "streaming":
            return Streaming()
        else:
            path0 = request.prepath.pop(0)
            request.postpath.insert(0, path0)
            return django
