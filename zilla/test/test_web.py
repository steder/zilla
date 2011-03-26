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


class Mock(object):
    def __getattr__(self, attr):
        return Mock()


class TestRootGetChild(unittest.TestCase):
    """getChild just does dynamic lookup of child
    resources.

    """

    def setUp(self):
        testServer = Mock()
        self.r = web.Root(testServer)

    def test_getRoot(self):
        """The root url should be handed off to wsgiResource
        """
        r = self.r.getChild("", None)
        self.assertEquals(r, web.django)

    def test_anythingElse(self):
        """Everything else is handed off to the wsgiResource

        """
        r = self.r.getChild("random.html", None)
        self.assertEquals(r, web.django)


class TestRoot_getChildWithDefault(unittest.TestCase):
    """getChildWithDefault is the the call that takes into
    account static resources and then calls getChild to
    check for dynamic resources.

    """
    def setUp(self):
        testServer = Mock()
        self.r = web.Root(testServer)

    def test_getRoot(self):
        """The root url should be handed off to wsgiResource
        """
        r = self.r.getChildWithDefault("", None)
        self.assertEquals(r, web.django)

    def test_anythingElse(self):
        """Everything else is handed off to the wsgiResource

        """
        r = self.r.getChildWithDefault("random.html", None)
        self.assertEquals(r, web.django)

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


