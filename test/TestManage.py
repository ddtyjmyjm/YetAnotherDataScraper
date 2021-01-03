import unittest
from click.testing import CliRunner
from src import manage
from src import config

class TestManage(unittest.TestCase):

    def test_get_metadata_and_manage(self):
        config_f = config.Config('./config.toml')

        m = manage.Manage(config_f)
        m.manage_main_mode()