#!/usr/bin/env python

from distutils.core import setup

try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    raise SystemExit("twisted not found.  Make sure you "
                     "have installed the Twisted core package.")

def refresh_plugin_cache():
    list(getPlugins(IPlugin))

if __name__ == '__main__':
    extraMeta = {}
    setup(name='Zilla',
          version='1.0',
          description='A Jukebox Server',
          author='Michael Steder',
          author_email='steder@gmail.com',
          url='https://bitbucket.org/steder/zilla',
          packages=[
            "zilla",
            "twisted.plugins",
            ],
          package_data={
            'twisted': ['plugins/zilla_plugin.py'],
            },
          setup_requires=[
            "Django==1.3",
            "Fabric==1.0.0",
            "South==0.7.3",
            "Twisted==10.2.0",
            "coverage==3.4",
            "distribute==0.6.15",
            "mock==0.7.0",
            "nose==1.0.0",
            "paramiko==1.7.6",
            "pycrypto==2.3",
            "wsgiref==0.1.2",
            "zope.interface==3.6.1",
            ]
          **extraMeta)
    refresh_plugin_cache()
