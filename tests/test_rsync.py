import unittest
from rsynco.libs.rsync import Rsync, NoHostException
from unittest.mock import Mock, MagicMock, patch, mock_open
import psutil
import os


class TestRsync(unittest.TestCase):
    def test_process_fails_with_no_hosts(self):
        rsync = Rsync()
        with self.assertRaises(NoHostException) as exit_code:
            rsync.process(None, '', None, '')

    @patch.object(os, 'wait')
    @patch.object(psutil, 'Popen')
    def test_process_starts_rsync_from_local_to_local_with_system_settings(self, mock_popen, mock_wait):
        rsync = Rsync()
        m = mock_open()

        with patch('rsynco.libs.rsync.open'.format(__name__), m, create=True):
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

        assert m.called
        assert m.call_count == 1
        mock_popen.called_once_with(['rsync', '--info=progress2', '--partial', '--recursive', '/', '/'], stdout=None)
        # assert mock_popen.called
        # assert mock_popen.call_count

    @patch.object(os, 'wait')
    @patch.object(psutil, 'Popen')
    def test_process_starts_rsync_from_local_to_remote_with_system_settings(self, mock_popen, mock_wait):
        rsync = Rsync()
        m = mock_open()

        with patch('rsynco.libs.rsync.open'.format(__name__), m, create=True):
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

        assert m.called
        assert m.call_count == 1
        assert mock_popen.called
        assert mock_popen.call_count
