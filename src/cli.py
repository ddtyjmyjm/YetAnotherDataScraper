from . import manage
from . import config
import click

CONFIG_FILE = './yads_config.toml'


@click.group()
def cli():
    """
    Grating
    """
    click.echo('YADS')


@cli.command()
@click.option('-c', '--config', 'config_file', type=click.File(encoding='UTF-8'))
@click.option('-r', '--resource', 'resource', type=click.Path(exists=True))
def scrape(config_file, resource):
    """
    Main command. Scrape info from folder or a file.
    """

    config_f = config.Config(config_file)
    if resource:
        # defined in option
        config_f.resource_folder = (lambda _: resource)
    manage_f = manage.Manage(config_f)

    manage_f.manage_main_mode()
    # todo: remove file or create symlink
