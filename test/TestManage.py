import unittest
from click.testing import CliRunner
from src import manage
from src import config

class TestManage(unittest.TestCase):

    def test_get_metadata_and_manage(self):
        config_f = config.Config('./yads_config.tom')

        m = manage.Manage(config_f)
        m.get_metadata_and_manage('ICDV-30245')