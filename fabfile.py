from fabric.api import local #, run


def test():
    local("nosetests --with-coverage --cover-package=zilla --verbose")
