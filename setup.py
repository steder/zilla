#!/usr/bin/env python

from setuptools import setup

REFRESH_PLUGINS = True
try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    REFRESH_PLUGINS = False
    print "Missing twisted..."

try:
    import yaml
except ImportError:
    REFRESH_PLUGINS = False

def refresh_plugin_cache():
    list(getPlugins(IPlugin))

import os

requirements_path = "./etc/requirements.txt"
print "requirements exists:", os.path.exists(requirements_path)
requirements = []
with open(requirements_path, "r") as requirements_file:
    print "requirements file", requirements_file
    for requirement in requirements_file:
        requirements.append(requirement.strip().rstrip())

print "requirements:"

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
      setup_requires=[],
      install_requires=requirements,
      **extraMeta)

if REFRESH_PLUGINS:
    refresh_plugin_cache()
