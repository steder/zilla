from twisted.trial import unittest

from zilla import settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.confFile = "/tmp/zilla_test.conf"
        tmpfile = open(self.confFile,"w")
        tmpfile.write("""# test config
host: testhost
port: 6666
databases: {"default":{"ENGINE":"django.db.backends.sqlite3",
                       "NAME":"test.db"}}
fake: Just Testing
        """)
        tmpfile.close()
        settings.load(self.confFile)

    def test_host(self):
        self.assertEqual(settings.HOST, 'testhost')

    def test_port(self):
        self.assertEqual(settings.PORT, 6666)

    def test_databases(self):
        self.assertEqual(settings.DATABASES, {"default":{"ENGINE":"django.db.backends.sqlite3", "NAME":"test.db"}})

    def test_fake(self):
        """The config machinery should only load expected config parameters"""
        self.assertEqual(True, "FAKE" not in settings.__dict__)

    def test_missingConfigFile(self):
        self.assertRaises(settings.ZillaSettingsError, settings.load, "/tmp/zilla_test_missing_file.test")



    
