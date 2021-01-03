from src.scrapers import u15dvdinfo
import pathlib
import shutil
import xml.etree.cElementTree as eT
import re
import click
import requests


class Manage:

    def __init__(self, config):
        self.config = config
        self.u15 = u15dvdinfo.U15DVDInfo()

    def scan_movies(self) -> list:
        """
        Scan movies from resource folder (loaded from config).
        Escape specified folders.
        """
        rsrc_path = pathlib.Path(self.config.resource_folder())
        suffixes = self.config.detect_suffixes()
        escapes = self.config.escape_folders()
        movie_list = [path for path in rsrc_path.glob("**/*")
                      if path.suffix in suffixes and path.stem not in escapes]
        return movie_list

    def parse_number(self, title):
        # todo: analysis title more safely and efficiency
        pattern = r'[a-zA-Z0-9]{1,}(-|_)[0-9]{1,}'
        return re.search(pattern, title).group(0)

    def _get_actors_str(self, information):
        try:
            actor_str = ','.join(information.get('actors'))
        except:
            actor_str = information.get('actors')[0]['name']
        return actor_str

    def _get_output_path(self, information):
        actors = self._get_actors_str(information)
        folder_path = pathlib.Path(self.config.managed_folder(),
                                   '[{}] - {} - {}'.format(information.get('number'),
                                                           actors,
                                                           information.get('title')))

        if not folder_path.is_absolute():
            return folder_path.resolve()
        else:
            return folder_path

    def write_poster(self, information, path):
        """Write poster"""

        url = information.get("poster_url")

        img = requests.get(url, stream=True)
        if img.status_code == 200:
            img.raw.decode_content = True
            content_type = img.headers['Content-Type'].split('/')[1]  # todo: better solution
            out_path = pathlib.Path(path, '{}.{}'.format(information.get('number'), content_type))
            with open(out_path, 'wb') as f:
                shutil.copyfileobj(img.raw, f)

    def write_kodi_nfo(self, information, path):
        """Write the provided information to movie.nfo."""
        click.echo("Writing movie.nfo...")
        root = eT.Element("movie")
        eT.SubElement(root, "title").text = information.get("title")
        eT.SubElement(root, "originaltitle").text = information.get("title")
        eT.SubElement(root, "sorttitle").text = '[{}] {} '.format(information.get("number"), information.get("title"))
        eT.SubElement(root, "premiered").text = information.get("premiered")
        eT.SubElement(root, "plot").text = information.get("plot")
        eT.SubElement(root, "studio").text = information.get("studio")
        for actor in information.get("actors"):
            sub = eT.SubElement(root, "actor")
            eT.SubElement(sub, "name").text = actor.get("name")
            eT.SubElement(sub, "type").text = "Actor"
        tree = eT.ElementTree(root)

        try:
            tree.write(pathlib.Path(path, information.get('number') + '.nfo'), encoding="UTF-8")
        except Exception as e:
            click.echo("Writing nfo failed!")
            click.echo(e)
        # print test
        # todo: show pretty xml

    def move_file_to_path(self, information,  rsrc: pathlib.Path, dist_folder: pathlib.PurePath):
        # todo: choose rename or not or there mode behaviour
        name = information.get("number") + rsrc.suffix
        dist = dist_folder.joinpath(name)
        rsrc.replace(dist)

    def write_symlink_file(self, information, url):
        # todo
        pass

    def manage_main_mode(self):
        # todo: remove or explict usage

        for rsrc_path in self.scan_movies():
            number = self.parse_number(rsrc_path.stem)
            raw_metadata = self.u15.get_result(number)

            try:
                dist_folder_path = self._get_output_path(raw_metadata)
                dist_folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                click.echo("Create scraped folder failed!")
                click.echo(e)
                from os import sys, EX_UNAVAILABLE
                sys.exit(EX_UNAVAILABLE)

            self.write_kodi_nfo(raw_metadata, dist_folder_path)
            self.write_poster(raw_metadata, dist_folder_path)
            self.move_file_to_path(raw_metadata, rsrc_path, dist_folder_path)

            print("finished")
