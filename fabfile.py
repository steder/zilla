from fabric.api import local #, run

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

def twisted_dev():
    static()
    local("twistd -n zilla")
