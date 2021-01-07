import requests
from bs4 import BeautifulSoup
import re


class U15DVDInfo:
    """scraper for U15DVDInfo"""

    __base_url = 'http://u15dvdinfo.com'

    def _metadata(self):
        return {
            'title': None,
            'studio': None,
            'number': None,
            'plot': None,
            'date': None,
            'country': 'Japan',
            'mpaa': 'R18',
            'poster_url': None,
            'actors': []
        }

    def search_product_url(self, title):
        """Low precision search using site's search engine."""

        # scraping
        payload = {'s_type': 'products', 's': title}
        index_page = requests.get(self.__base_url, params=payload).text

        # parsing
        soup = BeautifulSoup(index_page, 'html.parser')
        entry = soup.find_all("h2")
        if entry:
            return entry[0].find("a").get('href')  # todo: multiple choose
        else:
            return ""

    def number_to_url(self, number):
        """Get product url from title."""
        return '{}/products/{}'.format(self.__base_url, number)

    def number_to_p_url(self, number):
        """Get product picture url from title."""
        return 'http://u15dvd.jpn.org/p_image/{}'.format(number)

    def scrap_product_metadata(self, url):
        """Scrap product's metadata through confirmed url"""

        # scraping
        page = requests.get(url).text
        # parsing
        soup = BeautifulSoup(page, 'html.parser')
        text_body = soup.find(class_="textBody")
        metadata = self._metadata()
        metadata['poster_url'] = text_body.find(class_="p_image").find('img').get('src')
        metadata['plot'] = text_body.find(class_="description").get_text()
        pro_info = text_body.find(class_="pro_info")
        for tr in pro_info.find_all('tr'):
            tr_th = tr.th.get_text()
            tr_rd = tr.td.get_text()
            if tr_th == "商品名":
                metadata['title'] = tr_rd
            elif tr_th == "メーカー":
                metadata['studio'] = tr_rd
            elif tr_th == "品番":
                metadata['number'] = tr_rd
            elif tr_th == "発売日":
                metadata['date'] = re.sub(r"(\d+)年(\d+)月(\d+)日", r"\1-\2-\3", tr_rd)

        tr = text_body.find(class_="idol_info").find_all('tr')
        for tr in tr[1:]:
            td = tr.find('td')
            actor = {'name': td.get_text(), 'url': self.__base_url + td.next.get('href')}
            metadata['actors'].append(actor)

        return metadata

    def get_result(self, text):
        index_url = self.search_product_url(text)  # todo: more regex
        if index_url is None:
            return None
        else:
            return self.scrap_product_metadata(index_url)


if __name__ == "__main__":
    '''test'''
    number = 'bdzz-501'
    u15 = U15DVDInfo()
    # u15.get_result('bdzz-501')
    metadata = u15.scrap_product_metadata(u15.number_to_url(number))
    print("finish")
