__author__ = 'Martin Skytte'

from re import findall
from urllib import urlopen, quote
from pprint import pprint


class BoxOfficeMojo():

    def __init__(self):
        self.base_url = "http://www.boxofficemojo.com/"

    def _find_search_results(self, page):
        pattern = r'<a href="/movies/\?id\=([A-Za-z0-9\_\-]*?)\.htm">([A-Za-z0-9\_\- \&\:\?\.\(\)\'&amp;\!]*?)</a>'
        return [{link[1], link[0]} for link in findall(pattern, page)]

    def get_search_results(self, search_word):
        url = self.base_url + "search/?q=" + quote(search_word)
        page = urlopen(url)
        return self._find_search_results(page.read())

mojo = BoxOfficeMojo()
pprint(mojo.get_search_results("john"))