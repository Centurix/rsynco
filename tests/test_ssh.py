import unittest
from rsynco.libs.ssh import Ssh, PathNotFoundException
from unittest.mock import Mock, MagicMock, patch
import psutil


class TotException(Exception):
    pass


class TestSSH(unittest.TestCase):
    @patch.object(Ssh, 'local_listing')
    def test_ssh_uses_localhost_directory_iteration(self, mock_method):
        mock_method.return_value = "local"
        ssh = Ssh()
        assert ssh.get_contents('localhost', '/') == "local"

    @patch.object(Ssh, 'remote_listing')
    def test_ssh_uses_remotehost_directory_iteration(self, mock_method):
        mock_method.return_value = "remote"
        ssh = Ssh()
        assert ssh.get_contents('remotehost', '/') == "remote"

    def test_local_listing_returns_exception_when_path_does_not_exist(self):
        path = Mock()
        path.as_posix = Mock(return_value="posix_path")
        parent = Mock()
        parent.exists = Mock(side_effect=[True])
        path.parent = parent
        path.exists = Mock(side_effect=[False, False, True])

        ssh = Ssh()

        with self.assertRaises(PathNotFoundException) as context:
            contents = ssh.local_listing(path)
            assert contents == list()

    def test_local_listing_returns_one_file(self):
        path = Mock()
        path.as_posix = Mock(return_value="posix_path")
        path.exists = Mock(return_value=True)

        file_obj = Mock()
        file_obj.is_file = Mock(return_value=True)
        file_obj.is_dir = Mock(return_value=False)
        file_obj.is_symlink = Mock(return_value=False)
        file_obj.name = "file"

        path.iterdir = MagicMock(return_value=[file_obj])

        ssh = Ssh()
        contents = ssh.local_listing(path)

        assert contents == list([
            {'name': 'file', 'type': 'file'}
        ])

    def test_local_listing_returns_one_dir(self):
        path = Mock()
        path.as_posix = Mock(return_value="posix_path")
        path.exists = Mock(return_value=True)

        dir_obj = Mock()
        dir_obj.is_dir = Mock(return_value=True)
        dir_obj.is_file = Mock(return_value=False)
        dir_obj.is_symlink = Mock(return_value=False)
        dir_obj.name = "dir"

        path.iterdir = MagicMock(return_value=[dir_obj])

        ssh = Ssh()
        contents = ssh.local_listing(path)

        assert contents == list([
            {'name': 'dir', 'type': 'dir'}
        ])

    def test_local_listing_returns_one_link(self):
        path = Mock()
        path.as_posix = Mock(return_value="posix_path")
        path.exists = Mock(return_value=True)

        link_obj = Mock()
        link_obj.is_symlink = Mock(return_value=True)
        link_obj.is_dir = Mock(return_value=False)
        link_obj.is_file = Mock(return_value=False)
        link_obj.name = "link"

        path.iterdir = MagicMock(return_value=[link_obj])

        ssh = Ssh()
        contents = ssh.local_listing(path)

        assert contents == list([
            {'name': 'link', 'type': 'link'}
        ])

    def test_local_listing_returns_one_of_each_type(self):
        path = Mock()
        path.as_posix = Mock(return_value="posix_path")
        path.exists = Mock(return_value=True)

        file_obj = Mock()
        file_obj.is_file = Mock(return_value=True)
        file_obj.is_dir = Mock(return_value=False)
        file_obj.is_symlink = Mock(return_value=False)
        file_obj.name = "file"

        dir_obj = Mock()
        dir_obj.is_dir = Mock(return_value=True)
        dir_obj.is_file = Mock(return_value=False)
        dir_obj.is_symlink = Mock(return_value=False)
        dir_obj.name = "dir"

        link_obj = Mock()
        link_obj.is_symlink = Mock(return_value=True)
        link_obj.is_dir = Mock(return_value=False)
        link_obj.is_file = Mock(return_value=False)
        link_obj.name = "link"

        path.iterdir = MagicMock(return_value=[file_obj, dir_obj, link_obj])

        ssh = Ssh()
        contents = ssh.local_listing(path)

        assert contents == list([
            {'name': 'file', 'type': 'file'},
            {'name': 'dir', 'type': 'dir'},
            {'name': 'link', 'type': 'link'}
        ])

    @patch.object(psutil, 'Popen')
    def test_remote_listing_exists(self, mock_method):
        process = Mock()
        process.communicate = Mock(return_value=(b'stdout', b'No error'))
        mock_method.return_value = process
        path = Mock()
        path.as_posix = Mock(return_value='/')
        ssh = Ssh()
        result = ssh.remote_exists('remotehost', path)
        self.assertTrue(result)

    @patch.object(psutil, 'Popen')
    def test_remote_listing_does_not_exist(self, mock_method):
        process = Mock()
        process.communicate = Mock(return_value=(b'stdout', b'No such file or directory'))
        mock_method.return_value = process
        path = Mock()
        path.as_posix = Mock(return_value='/')
        ssh = Ssh()
        result = ssh.remote_exists('remotehost', path)
        self.assertFalse(result)

    @patch.object(psutil, 'Popen')
    def test_remote_directory_iteration(self, mock_method):
        process = Mock()
        process.communicate = Mock(return_value=(b'file1\nfile2\nfile3', b'stderr'))
        mock_method.return_value = process
        path = Mock()
        path.as_posix = Mock(return_value='/')
        ssh = Ssh()
        result = ssh.remote_iterdir('remotehost', path)
        assert result == list(['file1', 'file2', 'file3'])

    @patch.object(psutil, 'Popen')
    def test_remote_listing(self, mock_method):
        process = Mock()
        process.communicate = Mock(return_value=(b'one/\ntwo@\nthree*\nfour\n', b'stderr'))
        mock_method.return_value = process
        path = Mock()
        path.as_posix = Mock(return_value='/')
        ssh = Ssh()
        result = ssh.remote_listing('remotehost', path)
        assert result == list([{
            'type': 'dir',
            'name': 'one'
        }, {
            'type': 'link',
            'name': 'two'
        }, {
            'type': 'file',
            'name': 'three'
        }, {
            'type': 'file',
            'name': 'four'
        }])

    @patch.object(psutil, 'Popen')
    @patch.object(Ssh, 'remote_exists')
    @patch.object(Ssh, 'remote_iterdir')
    def test_remote_listing_iteration_does_not_exist(self, remote_iterdir, remote_exists, mock_method):
        process = Mock()
        process.communicate = Mock(return_value=(b'one/\ntwo@\nthree*\nfour\n', b'No such file or directory'))
        mock_method.return_value = process
        remote_exists.side_effect = [False, False, True]
        remote_iterdir.return_value = list([{
            'type': 'dir',
            'name': 'one'
        }, {
            'type': 'link',
            'name': 'two'
        }, {
            'type': 'file',
            'name': 'three'
        }, {
            'type': 'file',
            'name': 'four'
        }])
        path = Mock()
        path.as_posix = Mock(return_value='/')
        ssh = Ssh()

        with self.assertRaises(PathNotFoundException) as context:
            result = ssh.remote_listing('remotehost', path)
            assert result == list()
