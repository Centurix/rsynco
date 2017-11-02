import unittest
from rsynco.libs.rsync import Rsync


class TestRsync(unittest.TestCase):
    def test_process_fails_with_no_hosts(self):
        rsync = Rsync()
        rsync.process(None, '', None, '')