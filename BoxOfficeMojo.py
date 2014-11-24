__author__ = 'Martin Skytte'

from re import findall, finditer
from urllib import urlopen, quote
from itertools import islice
from pprint import pprint


class BoxOfficeMojo():
    """
    Class for getting earnings information about a movie from BoxOfficeMojo.com
    """

    def __init__(self):
        """
        Initialize base information for the class
        """
        self.base_url = "http://www.BoxOfficeMojo.com/"

    def _find_search_results(self, page):
        """
        Find a specific html pattern and return a list of BoxOfficeMojo page id names and readable names,
        from a given html page.

        :param page:
        :return list of dicts:
        """
        pattern = r'<a href="/movies/\?id\=([A-Za-z0-9\_\-]*?)\.htm">([A-Za-z0-9\_\- \&\:\?\.\(\)\'&amp;\!]*?)</a>'
        return [{link[1], link[0]} for link in findall(pattern, page)]

    def _find_earnings(self, page):
        """
        Find a specific html pattern and return a list of movie earnings, from a given html page.

        regex pattern is inspired by
        https://github.com/claudiob/boxoffice/blob/master/boxofficemojo.py

        :param page:
        :return list of ints:
        """
        pattern = r'<font color="#000080">\$([0-9,]*?)</font>'
        return [int(earning.replace(",", "")) for earning in findall(pattern, page)]

    def _find_first_seven_earnings(self, page):
        """
        Find a specific html pattern and return a list of the 7 first days of the movie earnings, from a given html page

        regex pattern is inspired by
        https://github.com/claudiob/boxoffice/blob/master/boxofficemojo.py

        :param page:
        :return list of ints:
        """
        pattern = r'<font color="#000080">\$([0-9,]*?)</font>'
        return [int(earning.group().replace(",", "").replace('<font color="#000080">$', "").replace("</font>", ""))
                for earning in islice(finditer(pattern, page, flags=0), 7)]

    def get_search_results(self, search_word):
        """
        Search for a movie using BoxOfficeMojos search engine. When given a word it will search the BoxOfficeMojo site
        
        :param search_word:
        :return list of dict:
        """
        url = self.base_url + "search/?q=" + quote(search_word)
        page = urlopen(url)
        return self._find_search_results(page.read())

    def get_movie_earnings(self, box_office_mojo_name):
        """
        Get all daily earnings from BoxOfficeMojo

        :param box_office_mojo_name: 
        :return list of ints:
        """
        url = self.base_url + "movies/?page=daily&id=" + box_office_mojo_name + ".htm"
        page = urlopen(url)
        return self._find_earnings(page.read())

    def get_first_seven_days(self, box_office_mojo_name):
        """
        Get first 7 days of earnings if available from BoxOfficeMojo

        :param box_office_mojo_name:
        :return list of ints:
        """
        url = self.base_url + "movies/?page=daily&id=" + box_office_mojo_name + ".htm"
        page = urlopen(url)
        return self._find_first_seven_earnings(page.read())

mojo = BoxOfficeMojo()
# pprint(mojo.get_search_results("john"))
# print mojo.get_movie_earnings("johnwick")
print mojo.get_first_seven_days("johnwick")