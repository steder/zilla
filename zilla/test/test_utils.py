"""Tests for zilla.utils

"""

import mock
from twisted.trial import unittest

from zilla import utils


class TestRingBuffer(unittest.TestCase):
    def setUp(self):
        self.rbSize = 13
        self.rb = utils.RingBuffer(self.rbSize)

    def test_append_1(self):
        self.rb.append("hello!")
        l = self.rb.toList()
        self.assertEquals(["hello!"], l)

    def test_append_to_capacity(self):
        for x in xrange(self.rbSize):
            self.rb.append(x)
        l = self.rb.toList()
        self.assertEquals(range(self.rbSize), l)

    def test_append_to_capacity_plus_1(self):
        for x in xrange(self.rbSize+1):
            self.rb.append(x)
        l = self.rb.toList()
        self.assertEquals(range(self.rbSize+1)[1:], l)
        
    def test_append_to_capacity_plus_capacity(self):
        for x in xrange(self.rbSize*2):
            self.rb.append(x)
        l = self.rb.toList()
        self.assertEquals(range(self.rbSize*2)[self.rbSize:], l)


class TestDecorators(unittest.TestCase):
    def f():
        pass

    @mock.patch("zilla.settings.DEBUG", new=True)
    def test_logFunctionTime_debugOn(self):
        wf = utils.logFunctionTime(TestDecorators.f)
        self.assertEquals("f_timedFunction", wf.__name__)
        
    @mock.patch("zilla.settings.DEBUG", new=False)
    def test_logFunctionTime_debugOff(self):
        wf = utils.logFunctionTime(TestDecorators.f)
        self.assertEquals(TestDecorators.f.__name__, wf.__name__)

    @mock.patch("zilla.settings.DEBUG", new=True)
    def test_logMethodTime_debugOn(self):
        class TestF(object):
            @utils.logMethodTime
            def f(self):
                pass
        self.assertEquals("f_timedMethod", TestF.f.__name__)
        
    @mock.patch("zilla.settings.DEBUG", new=False)
    def test_logMethodTime_debugOff(self):
        class TestF(object):
            @utils.logMethodTime
            def f(self):
                pass
        self.assertEquals("f", TestF.f.__name__)
        
