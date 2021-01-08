import unittest
from click.testing import CliRunner
from src import cli


class TestCli(unittest.TestCase):
    def test_scrape_c(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['scrape', '-c', 'config.toml'])
        print(result.stdout)

    def test_scrape_r(self):
        runner = CliRunner()
        result = runner.invoke(cli.cli, ['scrape', '-r', '../resrc'])
        print(result.stdout)
