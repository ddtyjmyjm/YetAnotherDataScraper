import toml
import click


class Config:

    def __init__(self, file):
        try:
            self.config = toml.load(file)
            click.echo("Loading config from " + file.name)

        except:
            self.config = None
            click.echo("Using default config!")

    def resource_folder(self):
        try:
            return self.config['management']['resource_folder']
        except:
            return 'resrc/'

    def managed_folder(self) -> str:
        try:
            return self.config['management']['managed_folder']
        except:
            return 'scraped/'

    def detect_suffixes(self) -> list:
        try:
            return self.config['rule']['detect_suffixes']
        except:
            return ['.webm', '.mkv', '.flv', '.avi', '.mts', '.m2ts', '.ts', '.3gp',
                    '.mov', '.wmv', '.rmvb', '.mp4', '.m4p', '.m4v', '.mpg', '.mpeg',
                    '.mpv', '.m2v', '.iso']

    def escape_folders(self) -> list[str]:
        try:
            return self.config['rule']["escape_folders"]
        except:
            return ['scraped/']
