import unittest
from click.testing import CliRunner
from src import cli
class TestCli(unittest.TestCase):



    def test_scrape_single_actor(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['scrape', 'ICDV-30245'])

    def test_scrape_double_actors(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['scrape', 'myt-047'])