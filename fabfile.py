from fabric.api import local #, run

def static():
    local("python zilla/manage.py collectstatic --noinput")

test_command = """DJANGO_SETTINGS_MODULE=zilla.settings PYTHONPATH="." %s --with-coverage --cover-package=zilla --with-django zilla --nocapture"""

def test():
    local(test_command % ("nosetests",))

def twisted_dev():
    static()
    local("twistd -n zilla")
