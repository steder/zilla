"""
Zilla Jukebox Server
"""
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from twisted.python import usage

from zope.interface import implements

from zilla import server


class Options(usage.Options):
    optFlags = [
        ["rotate", "r", "use daily log rotation instead of the default"]
    ]

    optParameters = [["port", "p", None, "port number to listen on."],
                     ["logfile", "l", "twistd.log", "file name to log to (ignored without --daily)"],
                     ["logdirectory", "d", ".", "path to directory for log files (ignored without --daily"]
                     ]

    
class ZillaServiceMaker(object):
    implements(IPlugin, IServiceMaker)
    tapname = "zilla"
    description = "Zilla Service"
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """
        from zilla import settings
        port = options["port"]
        if port is None:
            port = settings.PORT
        port = int(port)
        rotate = options["rotate"]
        logFile = options["logfile"]
        logDirectory = options["logdirectory"]
        madeServer = server.ZillaServer(port)
        madeServer.daily = bool(rotate)
        madeServer.logFile = logFile
        madeServer.logDirectory = logDirectory
        return madeServer


zilla = ZillaServiceMaker()
