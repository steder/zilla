"""test_web.py

Tests for the Zilla t.w.Resources
"""
from datetime import datetime

import mock
from twisted.trial import unittest
from twisted.web import resource, static
from twisted.web import server
from twisted.web._auth.wrapper import HTTPAuthSessionWrapper

from zilla import web


class TestRootGetChild(unittest.TestCase):
    """getChild just does dynamic lookup of child
    resources.

    """

    def setUp(self):
        testServer = mock.Mock()
        self.r = web.Root(testServer)

    def test_getRoot(self):
        """The root url should be handed off to wsgiResource
        """
        request = mock.Mock()
        request.prepath.pop.return_value = ""
        r = self.r.getChild("", request)
        self.assertEquals(r, web.django)
        request.postpath.insert.assert_called_with(0, "")


    def test_anythingElse(self):
        """Everything else is handed off to the wsgiResource

        """
        request = mock.Mock()
        request.prepath.pop.return_value = "test"
        r = self.r.getChild("test/random.html", request)
        self.assertEquals(r, web.django)
        request.postpath.insert.assert_called_with(0, "test")


class TestRoot_getChildWithDefault(unittest.TestCase):
    """getChildWithDefault is the the call that takes into
    account static resources and then calls getChild to
    check for dynamic resources.

    """
    def setUp(self):
        testServer = mock.Mock()
        self.r = web.Root(testServer)

    def test_getRoot(self):
        """The root url should be handed off to wsgiResource
        """
        request = mock.Mock()
        request.prepath.pop.return_value = ""
        r = self.r.getChildWithDefault("", request)
        self.assertEquals(r, web.django)
        request.postpath.insert.assert_called_with(0, "")

    def test_anythingElse(self):
        """Everything else is handed off to the wsgiResource

        """
        request = mock.Mock()
        request.prepath.pop.return_value = "test"
        r = self.r.getChildWithDefault("test/random.html", request)
        self.assertEquals(r, web.django)
        request.postpath.insert.assert_called_with(0, "test")

    def test_getStatic(self):
        """Urls including '/static/' should be served by
        the static directory web resource

        """
        r = self.r.getChildWithDefault("static", None)
        self.assertEquals(True, isinstance(r, static.File))

    def test_getFavicon(self):
        """The root '/favicon.ico' should be accessible

        """
        r = self.r.getChildWithDefault("favicon.ico", None)
        self.assertEquals(True, isinstance(r, static.File))


