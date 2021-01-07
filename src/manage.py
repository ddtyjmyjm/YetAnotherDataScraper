from src.scrapers import u15dvdinfo
import pathlib
import shutil
import xml.etree.ElementTree as ET
import re
import click
import requests


class Manage:

    def __init__(self, config):
        self.config = config
        self.u15 = u15dvdinfo.U15DVDInfo()

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

    def scan_movies(self) -> list:
        """
        *Deprecated*
        Scan movies from resource folder (loaded from config).
        Escape specified folders.
        """
        rsrc_path = pathlib.Path(self.config.resource_folder())
        suffixes = self.config.detect_suffixes()
        escapes = self.config.escape_folders()
        movie_list = [path for path in rsrc_path.glob("**/*")
                      if path.suffix in suffixes and path.stem not in escapes]
        return movie_list

    def scan_movies_and_analyze(self) -> dict:
        """
        Scan movies. Handle multiple pics
        like: - div
                - film-cd1
                - film-cd2
        """
        rsrc_path = pathlib.Path(self.config.resource_folder())
        suffixes = self.config.detect_suffixes()
        escapes = self.config.escape_folders()

        result = None
        for path in rsrc_path.glob("**/*"):
            if path.suffix not in suffixes \
                    or path.stem in escapes \
                    or path.match("._*.*"):   # afs file
                continue

            number = self.parse_number(path.stem)
            if result is None:
                result = {number: [path]}
            else:
                result[number] += [path]
        return result

    def write_assets(self, information, path):
        """Write posters, thumbs, fan arts ......"""

        url = information.get("poster_url")

        img = requests.get(url, stream=True)
        if img.status_code == 200:
            img.raw.decode_content = True
            content_type = img.headers['Content-Type'].split('/')[1]  # todo: better solution
            out_path = pathlib.PurePath(path, 'poster.' + content_type)
            with open(out_path, 'wb') as f:
                shutil.copyfileobj(img.raw, f)

    def write_kodi_nfo(self, information, path):
        """Write the provided information to movie.nfo."""
        click.echo("Writing movie.nfo...")
        root = ET.Element("movie")
        ET.SubElement(root, "title").text = information.get("title")
        ET.SubElement(root, "originaltitle").text = information.get("title")
        ET.SubElement(root, "sorttitle").text = '[{}] {} '.format(information.get("number"), information.get("title"))
        ET.SubElement(root, "premiered").text = information.get("premiered")  # KODI NFO standard
        ET.SubElement(root, "releasedate").text = information.get("premiered")  # Jellyfin readable NFO
        ET.SubElement(root, "country").text = information.get("country")
        ET.SubElement(root, 'mpaa').text = information.get("mpaa")
        ET.SubElement(root, "plot").text = information.get("plot")
        ET.SubElement(root, "studio").text = information.get("studio")
        for actor in information.get("actors"):
            sub = ET.SubElement(root, "actor")
            ET.SubElement(sub, "name").text = actor.get("name")
            ET.SubElement(sub, "type").text = "Actor"
        tree = ET.ElementTree(root)
        try:
            tree.write(pathlib.Path(path, information.get('number') + '.nfo'), encoding="UTF-8")
        except Exception as e:
            click.echo("Writing nfo failed!")
            click.echo(e)
        # print test
        # todo: show pretty xml

    def move_file_to_path(self, information, rsrc: pathlib.Path, dist_folder: pathlib.PurePath):
        # todo: choose rename or not or there mode behaviour
        name = information.get("number") + rsrc.suffix
        dist = dist_folder.joinpath(name)
        rsrc.replace(dist)

    def move_file_list_to_path(self, information, rsrc_list: [pathlib.Path], dist_folder: pathlib.Path):
        # todo : solution may cause wrong order
        number = information.get("number")
        if len(rsrc_list) == 1:
            rsrc = rsrc_list[0]
            name = number + rsrc.suffix
            rsrc.replace(dist_folder.joinpath(name))
        else:
            for idx, rsrc in enumerate(rsrc_list):
                name = number + "-cd" + str(idx + 1) + rsrc.suffix
                rsrc.replace(dist_folder.joinpath(name))

    def write_symlink_file(self, information, url):
        # todo
        pass

    def manage_main_mode(self):
        # todo: remove or explict usage

        for rsrc in self.scan_movies_and_analyze().items():
            number = rsrc[0]
            path_list = rsrc[1]
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
            self.write_assets(raw_metadata, dist_folder_path)
            self.move_file_list_to_path(raw_metadata, path_list, dist_folder_path)

            print("finished :" + raw_metadata.get("number"))
