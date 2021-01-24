import toml


class Config:
    DEFAULT_CONFIG_FILE = 'src/config.toml'

    def __init__(self, file):
        if file:
            try:
                self.config = toml.load(file)  # toml to dict
                print(f"Loading config from {file}")

            except Exception as e:
                print(f"Loading user config failed.")

        with open(self.DEFAULT_CONFIG_FILE) as file:
            self.default_config = toml.load(file)

    def get_attr(self, key_node, key_leaf):
        """Helper function to get attribute in config. """
        try:
            return self.config[key_node][key_leaf]
        except Exception as e:
            return self.default_config[key_node][key_leaf]

    def resource_folder(self):
        return self.get_attr("management", "resource_folder")

    def managed_folder(self) -> str:
        return self.get_attr('management', 'managed_folder')

    def detect_suffixes(self) -> list:
        return self.get_attr('rule', 'detect_suffixes')

    def escape_folders(self) -> list[str]:
        return self.get_attr('rule', "escape_folders")

    def scrapers(self):
        scraper_list = self.get_attr('rule', 'scrapers')
        scrapers_obj = list()
        for s in scraper_list:
            if s.lower() == 'u15dvdinfo':
                from scrapers import u15dvdinfo
                scrapers_obj.append(u15dvdinfo.U15DVDInfo)
        return scrapers_obj

    def scraper_mode(self):
        mode = self.get_attr('rule', 'scraper_mode')
        if mode != 'direct' and mode != 'auto':
            return 'auto'
        else:
            return mode
