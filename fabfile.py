from fabric.api import local #, run

def static():
    local("python zilla/manage.py collectstatic --noinput")

def test():
    local("nosetests --with-coverage --cover-package=zilla --verbose")

def twisted_dev():
    static()
    local("twistd -n zilla")
