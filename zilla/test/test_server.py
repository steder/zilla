import mock
from twisted.python import failure
from twisted.internet import reactor
from twisted.trial import unittest

from zilla import settings
from zilla import server

class TestZillaServer(unittest.TestCase):
    def test_serverName(self):
        self.server = server.ZillaServer(6667)
        webServer = self.server.getServiceNamed("Zilla")
        self.assertEqual("Zilla", webServer.name
                         )


class TestZillaServerStart(unittest.TestCase):
    @mock.patch("twisted.application.service")
    def setUp(self, mockTwistedApplicationService):
        self.stop = reactor.stop
        self.mockTwistedApplicationService = mockTwistedApplicationService
        portNumber = 6666
        self.server = server.ZillaServer(portNumber)
        self.server.shutdownHook = mock.Mock()

    def tearDown(self):
        reactor.stop = self.stop
        d = self.server.stopService()
        if self.server.started:
            self.server.shutdownHook.assert_called_with()
        return d

    def _startSuccess(self, result):
        self.assertEqual(True, result,
                         "Expect server start to return true result")
        return result

    def _startShouldNotFail(self, failure):
        self.fail("start should succeed!")
        return failure

    def _reactorShouldStop(self, result):
        return None

    def _startShouldFail(self, failure):
        self.assertTrue(failure is not None)

    def test_startService(self):
        self.server.startService()
        self.server.startDeferred.addCallbacks(callback=self._startSuccess,
                                               errback=self._startShouldNotFail)
        return self.server.startDeferred

    def test_startServiceFails(self):
        self.server.startService()

        d = self.server.startDeferred
        d.addCallbacks(callback=self._reactorShouldStop,
                       errback=self._startShouldFail)
        return d
        


