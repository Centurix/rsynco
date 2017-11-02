import unittest
from rsynco.libs.ssh import SshConfig
from unittest.mock import Mock, MagicMock


class TestSSHConfig(unittest.TestCase):
    def test_quit_parse_if_ssh_config_does_not_exist(self):
        mock_path = Mock()
        mock_path.is_file = MagicMock(return_value=False)

        ssh = SshConfig(mock_path)

        mock_path.is_file.assert_called_once_with()

        assert ssh.hosts == list()

    def test_empty_ssh_config_returns_no_hosts(self):
        mock_path = Mock()
        mock_path.is_file = MagicMock(return_value=True)
        mock_path.open = MagicMock()

        ssh = SshConfig(mock_path)

        assert ssh.hosts == list()

    def test_reading_ssh_config_returns_multiple_hosts(self):
        mock_path = Mock()
        mock_path.is_file = MagicMock(return_value=True)

        open_mock = MagicMock()
        file_mock = MagicMock()
        file_mock.readlines = Mock(return_value=[
            "Host Homestead\n",
            "\tHostName 127.0.0.1\n",
            "\tUser vagrant\n",
            "\tPort 2222\n",
            "Host Homestead2\n",
            "\tHostName 127.0.0.1\n",
            "\tUser vagrant\n",
            "\tPort 2222\n"
        ])
        open_mock.__enter__ = Mock(return_value=file_mock)
        mock_path.open = MagicMock(return_value=open_mock)

        ssh = SshConfig(mock_path)

        assert ssh.hosts == list([{
            'host': 'Homestead',
            'hostname': '127.0.0.1',
            'port': 2222,
            'username': 'vagrant',
            'password': '',
            'type': 'system'
        }, {
            'host': 'Homestead2',
            'hostname': '127.0.0.1',
            'port': 2222,
            'username': 'vagrant',
            'password': '',
            'type': 'system'
        }])

    def test_reading_malformed_ssh_config_returns_no_hosts(self):
        mock_path = Mock()
        mock_path.is_file = MagicMock(return_value=True)

        open_mock = MagicMock()
        file_mock = MagicMock()
        file_mock.readlines = Mock(return_value=[
            "HostHomestead\n",
            "\tHostName127.0.0.1\n",
            "\tUservagrant\n",
            "\tPort2222\n"
        ])
        open_mock.__enter__ = Mock(return_value=file_mock)
        mock_path.open = MagicMock(return_value=open_mock)

        ssh = SshConfig(mock_path)

        assert ssh.hosts == list()

    def test_reading_ssh_config_with_missing_hostname_returns_no_hosts(self):
        mock_path = Mock()
        mock_path.is_file = MagicMock(return_value=True)

        open_mock = MagicMock()
        file_mock = MagicMock()
        file_mock.readlines = Mock(return_value=[
            "Host Homestead\n",
            "\tUser vagrant\n",
            "\tPort 2222\n"
        ])
        open_mock.__enter__ = Mock(return_value=file_mock)
        mock_path.open = MagicMock(return_value=open_mock)

        ssh = SshConfig(mock_path)

        assert ssh.hosts == list()

    def test_reading_ssh_config_with_bare_minimum_details_return_a_host_with_default_values(self):
        mock_path = Mock()
        mock_path.is_file = MagicMock(return_value=True)

        open_mock = MagicMock()
        file_mock = MagicMock()
        file_mock.readlines = Mock(return_value=[
            "Host Homestead\n",
            "\tHostName 127.0.0.1\n",
        ])
        open_mock.__enter__ = Mock(return_value=file_mock)
        mock_path.open = MagicMock(return_value=open_mock)

        ssh = SshConfig(mock_path)

        assert ssh.hosts == list([{
            'host': 'Homestead',
            'hostname': '127.0.0.1',
            'port': 22,
            'username': '',
            'password': '',
            'type': 'system'
        }])
