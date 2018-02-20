import unittest
from rsynco.libs.rsync import Rsync, NoHostException
from unittest.mock import Mock, MagicMock, patch, mock_open
import psutil
import os
import tempfile


class TestRsync(unittest.TestCase):
    def test_process_fails_with_no_hosts(self):
        rsync = Rsync()
        with self.assertRaises(NoHostException) as exit_code:
            rsync.process(None, '', None, '')

    @patch.object(tempfile, 'NamedTemporaryFile')
    @patch.object(os, 'wait')
    @patch.object(psutil, 'Popen')
    def test_process_starts_rsync_from_local_to_local_with_system_settings(self, mock_popen, mock_wait, mock_temp):
        rsync = Rsync()

        rsync.process(
            {
                'type': 'system',
                'host': '',
                'hostname': 'localhost'
            }, '/', {
                'type': 'system',
                'host': '',
                'hostname': 'localhost'
            }, '/'
        )

        assert mock_wait.call_count == 2
        assert mock_temp.call_count == 1
        assert mock_popen.call_count == 2

    @patch.object(tempfile, 'NamedTemporaryFile')
    @patch.object(os, 'wait')
    @patch.object(psutil, 'Popen')
    def test_process_starts_rsync_from_local_to_remote_with_system_settings(self, mock_popen, mock_wait, mock_temp):
        rsync = Rsync()

        rsync.process(
            {
                'type': 'system',
                'host': '',
                'hostname': 'localhost'
            }, '/', {
                'type': 'system',
                'host': '',
                'hostname': 'remote_host'
            }, '/'
        )

        assert mock_wait.call_count == 2
        assert mock_temp.call_count == 1
        assert mock_popen.call_count == 2
