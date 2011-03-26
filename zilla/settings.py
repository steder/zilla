"""
The standard django settings module.

Includes a number of values specific to the
Twisted service that is serving as a WSGI container.

"""

from twisted.python import filepath

# begin zilla settings
# When running behind apache we need to know what the base URL for the textura resources will be.
STATIC_HOST = "localhost"
STATIC_PORT = 80
DEBUG = False
DEBUG_PASSWORD="password"
DEFER_DEBUG = False
HOST = None
MODE = None
POOL = None
PORT = 8080
PROCESS_DEBUG = False
PROCESS_TIMEOUT = 30 # seconds until timeout
# this string is what to look for in the child process output
# to identify when the child process is ready to go
READY = None

ZILLA_ROOT = filepath.FilePath(__file__).parent().parent()
TEMPLATE_DIR = ZILLA_ROOT.child("zilla").child("templates").path
ADMIN_PASSWORD_FILE = ZILLA_ROOT.child("etc").child("passwd.conf").path

TEST_BIN = ZILLA_ROOT.child("bin").child("zillaChild.py")

# end zilla settings
# begin ledware settings

# Ed probably wants to call this "ledware":
# This webware-a-like needs to know where to find textura CPM and its servlets:
TEXTURA_ROOT = ZILLA_ROOT
TEXTURA_PATH = TEXTURA_ROOT.child('textura') #ZILLA_ROOT.child("textura")
SERVLET_PATH = TEXTURA_PATH.child("Web")

SESSION_PREFIX = ''
SESSION_TIMEOUT = 60
SESSION_NAME = '_SID_'
SESSION_STORE_MODULE = 'zilla.led.sessionstore.SessionFileStore'
SESSION_MODULE = 'zilla.led.session.Session'
SESSION_USE_AUTOMATIC_PATH_SESSIONS = False
SESSION_DEBUG = False
SESSION_IGNORE_INVALID_SETTING = False
SESSION_USE_COOKIE_SESSIONS = True
SECURE_SESSION_COOKIE = False
SESSION_DIR = ZILLA_ROOT.child("session").path
SESSION_COOKIE_PATH = None

CONTEXTS = {}
DEFAULT_CONTEXT = 'textura'
LOG_ACTIVITY = True
VERSION = 1
VERSION_STRING = '1 freakin 0 detroit rock city!'
LOG_ACTIVITY = False
ERROR_404 = 'error404.html'
ERROR_PAGE = None
ENTER_DEBUGGER_ON_EXCEPTION = False



