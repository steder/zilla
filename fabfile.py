import os
from fabric.api import local #, run

def create_config():
    if not os.path.exists("zilla.conf"):
        local("cp etc/development.conf zilla.conf")

def static():
    local("python zilla/manage.py collectstatic --noinput")

def test():
    test_command = """DJANGO_SETTINGS_MODULE=zilla.settings PYTHONPATH="." nosetests --with-django zilla --nocapture"""
    local(test_command)

def coverage():
    coverage_command = """DJANGO_SETTINGS_MODULE=zilla.settings PYTHONPATH="." nosetests --with-coverage --cover-package=zilla --with-django zilla --nocapture"""
    local(coverage_command)

def nosy():
    command = """DJANGO_SETTINGS_MODULE=zilla.settings PYTHONPATH="." nosy -c  etc/nosy.cfg"""
    local(command)

def dependencies():
    local("pip install -r etc/requirements.txt")

def init():
    local("python zilla/manage.py syncdb")

def install():
    dependencies()
    create_config()
    test()
    init()

def devserver():
    static()
    local("twistd -n zilla")

def daemon():
    static()
    local("twistd zilla")
    
