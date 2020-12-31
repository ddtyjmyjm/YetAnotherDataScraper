import toml


class Config:

    def __init__(self, path):
        try:
            file = open(path, 'r')
            self.config = toml.load(file)
        except:
            self.config = None

    def resource_folder(self):
        try:
            return self.config['management']['resource_folder']
        except:
            return 'resrc/'

    def managed_folder(self):
        try:
            return self.config['management']['managed_folder']
        except:
            return 'scraped/'
