import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Spider:

    host = ''

    def __init__(self):
        self.session = self.get_session()

    @staticmethod
    def get_session():
        session = requests.Session()
        ua = UserAgent()
        h = {
            'User-Agent': ua.random
        }
        session.headers.update(h)

        return session

    def get_html(self, url: str, json_data: bool=False, host: bool=True):
        response = self.session.get(url=self.host + url if host else url)
        if response.status_code != 200:
            raise ValueError(f'status_code != 200: {url}')
        # на случай проблем с кодировкой ответа
        response.encoding = response.apparent_encoding

        if json_data:
            return response.json()

        return response.text

    @staticmethod
    def get_bs(html_text):
        return BeautifulSoup(html_text, 'html.parser')
