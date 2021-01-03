# YADS
Yet Another Data Scraper

# build
> :warning: `python3` >= 3.8 is required. Otherwise, unknown behavior may occur. 

If pip >= 19.0
```bash
pip3 install .
```
If 10.0 <= pip <= 19.0
```bash
python3 setup.py install
```

# Usage

## cli
```
yads-cli scrape [-c config_file] [-r resource_folder_path]
```
## config file
Using `-c` option to choose config file which is a `toml` file.

### management
About folder path.

1. `resource_folder`: resource folder which needed to be managed. Default is `'resrc/'`
2. `managed_folder`: output folder. Default is `'scraped/'`

### rule
About management behavior.

1. `detect_suffixes` : Movies' suffixes.
2. `escape_folders`: Escape folders that scan the resource folder.
