import collections
import md5, os, random, time
import re, sys, traceback, urllib

from timeit import default_timer

from twisted.python import log

from zilla import settings


class RingBuffer(collections.deque):
    def __init__(self, size_max):
        collections.deque.__init__(self)
        self.size_max = size_max
    def append(self, datum):
        collections.deque.append(self, datum)
        if len(self) > self.size_max:
            self.popleft( )
    def toList(self):
        return list(self)


def logFunctionTime(function):
    if settings.DEBUG:
        def timedFunction(*args, **kwargs):
            start = default_timer()
            result = function(*args, **kwargs)
            end = default_timer() - start
            log.msg(
                '%s.%s executed in %f seconds' % (
                    function.__module__, function.__name__, end
                )
            )
            return result
        timedFunction.__name__ = "%s_timedFunction"%(function.__name__,)
        return timedFunction
    else:
        return function


def logMethodTime(method):
    if settings.DEBUG:
        def timedMethod(self, *args, **kwargs):
            start = default_timer()
            result = method(self, *args, **kwargs)
            end = default_timer() - start
            log.msg(
                '%s.%s.%s executed in %f seconds' % (
                    method.__module__,
                    self.__class__.__name__,
                    method.__name__,
                    end
                )
            )
            return result
        timedMethod.__name__ = "%s_timedMethod"%(method.__name__,)
        return timedMethod
    else:
        return method


def roundrobin(*iterables):
    pending = collections.deque(iter(i) for i in iterables)
    while pending:
        task = pending.popleft()
        try:
            yield task.next()
        except StopIteration:
            continue
        pending.append(task)


