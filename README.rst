Zilla Jukebox
------------------------------------------------

Zilla Jukebox is a simple server for server music on the internet or your local network.

A jukebox owner can add albums and songs to their Jukebox.  Both owners and listeners can search for
and browse these albums and songs.

Requirements
------------------------------------------------

Zilla was developed on Mac OS X (10.6) and has also
been tested and deployed on Ubuntu Linux.  Any *NIX
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
Nosy_, South_, and Mutagen_.

Installation
-------------------------------------------------

NOTE - ZILLA_ROOT::

  The directory that contains this file is the ZILLA_ROOT directory.

  Instructions will refer to this directory wherever possible to make it clear
  where commands should be executed.

0. Optional: create a virtualenv::
 a. With virtualenvwrapper:
   $ mkvirtualenv zilla 
 b. with just plain virtualenv
   $ mkdir ~/virtualenvs virtualenv ~/.virtualenvs/zilla
   $ source ~/.virtualenvs/zilla/bin/activate
 
1. Install Python Dependencies::
  Let's use Pip and Fabric:
   $ cd $ZILLA_ROOT
   $ easy_install pip
   $ pip install fabric
   $ fab install

"fab install" will:
 1. install the rest of the dependencies with Pip
 2. copy the default configuration to ZILLA_ROOT/zilla.conf
 3. Run the test suite
 4. And if everything runs cleanly it'll create an initial database.

Running the service
----------------------------------

$ cd $ZILLA_ROOT
$ fab devserver

Running the service daemonized for production
------------------------------------------------------

$ fab daemon

Checking the daemonized services logs:
------------------------------------------------------

 $ tail -f $ZILLA_ROOT/twistd.log

Shutting down the daemonized service:
------------------------------------------------------

 $ kill `cat zilla.pid`



