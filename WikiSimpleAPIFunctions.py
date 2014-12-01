# -*- coding: utf-8 -*-
__author__ = 'Martin Skytte'

from urllib2 import urlopen, quote, unquote
from json import load
from xml.dom import minidom
from datetime import datetime


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
        url = self.base_url + "opensearch&format=xml&search=" + quote(search_term)
        page_data = urlopen(url)
        xml = minidom.parse(page_data)
        return {node.getElementsByTagName("Text")[0].firstChild.data: dict(
            description=node.getElementsByTagName("Description")[0].firstChild.data,
            url=node.getElementsByTagName("Url")[0].firstChild.data.rsplit("/", 1)[1])
            for node in xml.getElementsByTagName("Item")}

    def page_created_date(self, page_name):
        """Returns the first date the revision of a page from Wikipedia, which is the
        date a Wikipedia page is created.

        :param page_name:
        :return datetime:
        """
        url = self.base_url + "query&rawcontinue=true&prop=revisions&rvprop=timestamp&" \
                              "rvdir=newer&rvlimit=1&format=json&titles=" + page_name
        page_data = urlopen(url)
        json_object = load(page_data)
        revisions = json_object['query']['pages'].values()[0]
        date = None
        if "revisions" not in revisions:
            print "key not found"
        else:
            date = datetime.strptime(revisions['revisions'][0]['timestamp'], "%Y-%m-%dT%H:%M:%SZ")

        return date