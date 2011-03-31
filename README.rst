Zilla Jukebox
------------------------------------------------

Zilla Jukebox is a simple server for server music on the internet or your local network.

A jukebox owner can add albums and songs to their Jukebox.  Both owners and listeners can search for
and browse these albums and songs.

Requirements
------------------------------------------------

Zilla was developed on Mac OS X (10.6) and has also
been tested and deployed on Ubuntu Linux.  Any \*NIX
environment with a recent (2.6+) version of Python
should be able to run Zilla.  Zilla is not yet compatible
with Python3_.

So assuming you have a compatible operating system you'll
also need the following.

You will need one of each of the following:

 - Python Version: Python 2.6, Python 2.7
 - Easy_Install and Setuptools or a willingness to download
   and compile python packages from PyPI_
 - DB API Driver: sqlite3_, psycopg2_, etc

You will then need to install the following packages.

PIP_ and VirtualEnv_ (and VirtualEnvWrapper_) are recommended but not required.

See etc/requirements.txt for all required Python packages and versions.

The core packages are Django_, Twisted_, BeautifulSoup_, PyYaml_, and Nose.

For convenience and future extension I've included Fabric_, NoseDjango_,
Nosy_, and South_.

Installation
-------------------------------------------------

NOTE - ZILLA_ROOT::

  The directory that contains this file (`README.rst`) is the ZILLA_ROOT directory.

  Instructions will refer to this directory wherever possible to make it clear
  where commands should be executed.

1. Optional: create a virtualenv
============================================

a. With virtualenvwrapper
::

  $ mkvirtualenv zilla 

b. with just plain virtualenv
::
    
  $ mkdir ~/virtualenvs virtualenv ~/.virtualenvs/zilla
  $ source ~/.virtualenvs/zilla/bin/activate
    
 
2. Install Python Dependencies
============================================

Let's use Pip and Fabric

    $ cd $ZILLA_ROOT
    $ easy_install pip
    $ pip install fabric
    $ fab install

"fab install" will::

  1. install the rest of the dependencies with Pip
  2. copy the default configuration to ZILLA_ROOT/zilla.conf
  3. Run the test suite
  4. And if everything runs cleanly it'll create an initial database.

Optional: Configure DB settings to use PostgreSQL
======================================================

  edit $ZILLA_ROOT/zilla.conf and add

  ::
  
    # You'll want to substitute your own values for at least
    # NAME, USER, and PASSWORD below.
   
    databases:
      default:
        ENGINE: 'django.db.backends.postgresql_psycopg2'
        NAME: 'zilla'
        USER: 'steder'
        PASSWORD: 'password'
        HOST: 'localhost'
        PORT: '5432'

  Install Psycopg2:

  ::
  
    $ pip install pyscopg2

  Create the zilla db and create the initial schema and superuser account:

  ::
  
    $ cd $ZILLA_ROOT
    $ createdb zilla
    $ python zilla/manage.py syncdb
    
Installing Fixture Data to quickly get a sample Jukebox Running
=================================================================

If you're interested in just quickly checking out what Zilla Jukebox
looks like you'll maybe be interested in a small sample dataset you
can load.

After running syncdb just do the following

::

  $ python zilla/manage.py loaddata etc/sample_fixture.json

Now you'll have a small collection of artists, albums, and songs.

Running the service
----------------------------------

You'll run the server for development or testing with the following
command:

::

 $ cd $ZILLA_ROOT
 $ fab devserver

Running the service daemonized for production
===============================================

To run it as a service you'll do:

::

 $ fab daemon

This handles putting the process in the background, writing
a PID file so you can find and kill this process later,
and setting up logging.

Checking the daemonized services logs:
===============================================

To check out your logs while the server is daemonized
you can simply tail the zilla.log file.

::

 $ tail -f $ZILLA_ROOT/zilla.log

Shutting down the daemonized service:
==============================================

To shut down the daemonized service you just need to send
the kill signal to the process.  You can accomplish that
pretty easily with the following one liner.

::

 $ kill `cat zilla.pid`


.. _python3: http://www.python.org/download/releases/3.2/
.. _pypi: http://pypi.python.org/
.. _sqlite3: http://www.sqlite.org/
.. _psycopg2: http://www.initd.org/psycopg/
.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _django: http://www.djangoproject.com/
.. _twisted: http://www.twistedmatrix.com/
.. _beautifulsoup: http://www.crummy.com/software/BeautifulSoup/
.. _pyyaml: http://pyyaml.org/
.. _fabric: http://docs.fabfile.org/en/1.0.1/index.html
.. _nosedjango: http://pypi.python.org/pypi/NoseDjango/0.8.1
.. _nosy: http://pypi.python.org/pypi/nosy/1.1
.. _south: http://south.aeracode.org/


