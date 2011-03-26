#-*- test-case-name: zilla.test.test_web -*-
import os

from twisted.internet import reactor
from twisted.web import http, resource, server, static
from twisted.web import wsgi

#from txtemplate import templates
from zilla import settings
from zilla import utils
from zilla import whiskey

staticDirectory = static.File(
    settings.STATIC_ROOT
)


django = wsgi.WSGIResource(reactor, reactor.getThreadPool(),
                           whiskey.application)


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
        if path == "hello":
            return self
        else:
            path0 = request.prepath.pop(0)
            print "path0:", path0
            request.postpath.insert(0, path0)
            return django
