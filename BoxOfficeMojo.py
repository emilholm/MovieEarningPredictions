__author__ = 'Martin Skytte'

from re import findall, finditer, search
from urllib import urlopen, quote
from itertools import islice
from datetime import datetime
from BoxOfficeMojoException import BoxOfficeMojoException


class BoxOfficeMojo():
    """
    Class for getting earnings information about a movie from BoxOfficeMojo.com
    """

    def __init__(self):
        """
        Initialize base information for the class
        """
        self.base_url = "http://www.BoxOfficeMojo.com/"

    def _find_release_date(self, page):
        """
        Find a specific html pattern and return the release date from BoxOfficeMojo, given html page.

        :param page:
        :return:
        """
        pattern = r'<a href="/schedule/\?view=bydate&release=theatrical&date\=([0-9]{4}-[0-9]{2}-[0-9]{2})'
        return search(pattern, page)

    def _find_search_results(self, page):
        """
        Find a specific html pattern and return a list of BoxOfficeMojo page id names and readable names,
        from a given html page.

        :param page:
        :return list of dicts:
        """
        pattern = r'<a href="/movies/\?id\=([A-Za-z0-9\_\-]*?)\.htm">([A-Za-z0-9\_\- \&\:\?\.\(\)\'&amp;\!]*?)</a>'
        return {link[1]: link[0] for link in findall(pattern, page)}

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
        results = self._find_search_results(page.read())
        if not results:
            raise BoxOfficeMojoException("No search results found on BoxOfficeMojo.com")
        return results

    def get_movie_earnings(self, box_office_mojo_name):
        """
        Get all daily earnings from BoxOfficeMojo

        :param box_office_mojo_name: 
        :return list of ints:
        """
        url = self.base_url + "movies/?page=daily&id=" + box_office_mojo_name + ".htm"
        page = urlopen(url)
        results = self._find_earnings(page.read())
        if not results:
            raise BoxOfficeMojoException("Either the movies does not exists on BoxOfficeMojo.com, haven't had premiere "
                                         "or the id of the movie is wrong, try correcting the box_office_mojo_name")
        return results

    def get_first_seven_days(self, box_office_mojo_name):
        """
        Get first 7 days of earnings if available from BoxOfficeMojo

        :param box_office_mojo_name:
        :return list of ints:
        """
        url = self.base_url + "movies/?page=daily&id=" + box_office_mojo_name + ".htm"
        page = urlopen(url)
        results = self._find_first_seven_earnings(page.read())
        if not results:
            raise BoxOfficeMojoException("Either the movies does not exists on BoxOfficeMojo.com, haven't had premiere "
                                         "or the id of the movie is wrong, try correcting the box_office_mojo_name")
        return results

    def get_release_date(self, box_office_mojo_name):
        """
        Find the release date for a movie, given the BoxOfficeMojo name of a film

        :param box_office_mojo_name:
        :return datetime:
        """
        url = self.base_url + "movies/?id=" + box_office_mojo_name + ".htm"
        page = urlopen(url)
        result = self._find_release_date(page.read())
        if result is None:
            raise BoxOfficeMojoException("Either the movies does not exists on BoxOfficeMojo.com or the id of "
                                         "the movie is wrong, try correcting the box_office_mojo_name")
        date_obj = datetime.strptime(result.group(1), "%Y-%m-%d")
        return date_obj