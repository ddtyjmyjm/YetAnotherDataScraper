from . import manage
from . import config
import click

CONFIG_FILE = './yads_config.toml'


@click.group()
def cli():
    """test script"""
    click.echo('Hello World!')


@cli.command()
@click.argument('title', type=str)
@click.option('-c', '--config', 'config_path', type=str, default=CONFIG_FILE)
def scrape(title, config_path):
    config_f = config.Config(config_path)
    manage_f = manage.Manage(config_f)
    manage_f.get_metadata_and_manage(title)
