import unittest
from click.testing import CliRunner
from src import cli


class TestCli(unittest.TestCase):
    def test_scrape(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['scrape','-c','yads_config.toml'])
        print(result.stdout)
