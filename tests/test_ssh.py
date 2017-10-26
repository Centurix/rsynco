import unittest
from rsynco.libs.ssh import SshConfig
from pathlib import Path


class TestSSH(unittest.TestCase):
    def test_new_host(self):
        file_path = Path('')
        ssh = SshConfig(file_path)
        new_host = ssh.new_host()
        self.assertEqual(new_host, {
            'host': '',
            'hostname': '',
            'port': 22,
            'username': '',
            'password': '',
            'type': 'system'
        })
