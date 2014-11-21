__author__ = 'Martin Skytte'

from urllib2 import urlopen, quote
from json import load, dumps


class WikiSimpleAPIFunctions:
    """Class for making simple requests to the Wikipedia API"""

    def __init__(self):
        """Initialize the basic url for the Wikipedia API"""
        self.base_url = "https://en.wikipedia.org/w/api.php?action="

    def search_suggestions(self, search_term):
        """Returns a list of suggestions from Wikipedia, based on the given search term

        :param search_term:
        :return list:
        """
        url = self.base_url + "opensearch&search=" + quote(search_term)
        page_data = urlopen(url)
        json_object = load(page_data)
        return json_object[1]

    def page_created_date(self, page_name):
        """

        :param page_name:
        :return:
        """
        url = self.base_url + "query&rawcontinue=true&prop=revisions&rvprop=timestamp&" \
                              "rvdir=newer&rvlimit=1&format=json&titles=" + quote(page_name)
        page_data = urlopen(url)
        json_object = load(page_data)
        return json_object

wiki = WikiSimpleAPIFunctions()
list = wiki.search_suggestions("j")
print list
list = wiki.search_suggestions("jo")
print list
list = wiki.search_suggestions("joh")
print list
list = wiki.search_suggestions("john")
print list
list = wiki.search_suggestions("john wick")
print list
list = wiki.search_suggestions("me myself")
print list

created_date = wiki.page_created_date("John_Wick_(film)")
print dumps(created_date, sort_keys=True, indent=4, separators=(',', ': '))