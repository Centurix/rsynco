import unittest
from rsynco import Config
from unittest.mock import Mock, patch


class TestConfig(unittest.TestCase):
    @patch('rsynco.ConfigObj')
    @patch('rsynco.Validator')
    def test_valid_file(self, validator_object, config_object):
        config_object.validate.return_value = False
        config = Config('test_file', 'test_spec')
        assert config.data is not None

    # def test_invalid_file(self):
    #     pass
    #
    # def test_valid_spec(self):
    #     pass
    #
    # @patch('rsynco.ConfigObj')
    # @patch('rsynco.Validator')
    # def test_invalid_spec(self, validator_object, config_object):
    #     config_object.validate = Mock(return_value=False)
    #     config = Config('test_file', 'test_spec')
    #
    #     assert config.data is None

    # def test_validation_pass(self):
    #     pass
    #
    # def test_validation_fail(self):
    #     pass
    #
    # def test_update(self):
    #     pass
    #
    # def test_refresh(self):
    #     pass
