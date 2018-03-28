import unittest
from unittest.mock import Mock, MagicMock, patch
from rsynco.libs.daemon import Daemon


class TestDaemon(unittest.TestCase):
    @patch('rsynco.libs.daemon.os')
    def test_daemonize_first_fork_success(self, os_object):
        os_object.fork = Mock(return_value=1)
        daemon = Daemon('test_pid')
        with self.assertRaises(SystemExit) as exit_code:
            daemon.daemonize()

        self.assertEqual(exit_code.exception.code, 0)

    @patch('rsynco.libs.daemon.os')
    def test_daemonize_second_fork_success(self, os_object):
        os_object.fork = Mock(side_effect=[0, 1])
        daemon = Daemon('test_pid')
        with self.assertRaises(SystemExit) as exit_code:
            daemon.daemonize()

        self.assertEqual(exit_code.exception.code, 0)

    # @patch('rsynco.libs.daemon.os')
    # @patch('rsynco.libs.daemon.sys')
    # @patch('rsynco.libs.daemon.atexit')A
    # def test_daemonize_test_registered_process(self, atexit_object, sys_object, os_object):
    #     os_object.fork = Mock(side_effect=[0, 0])
    #     os_object.getpid = Mock(return_value=1)
    #     daemon = Daemon('test_pid')
    #     daemon.daemonize()
