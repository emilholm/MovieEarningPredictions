__author__ = 'Martin Skytte'

from urllib2 import urlopen
from json import load
from datetime import datetime
from dateutil import rrule


class WikiPageViews():
    """Get the page views from for a specific wiki site, will only get to the page creation date."""

    def __init__(self, base_url="http://stats.grok.se/json/en/"):
        """Initiate variables used in the class, the base_url is the url for the for getting the page views.
        By default it uses the swedish site http://stats.grok.se/json/en/ as base url."""

        self.baseUrl = base_url

    def get_current_month_page_views(self, name):
        """Gets the current months page views for a Wikipedia page, given the Wikipedia url page name.

        example:
        John_Wick_(film)

        :param name:
        :return json:"""

        return self.get_page_views_from_name_year_month(name, datetime.today().strftime("%Y%m"))

    def get_page_views_from_name_year_month(self, name, year_month):
        """Get page views for a wiki page with a given name and year_month.

        name must be in the wiki url format:
        John_Wick_(film)

        year_month must be in the format of:
        %Y%m
        example:
        201308

        :param name:
        :param year_month:
        :return json:"""

        url = self.baseUrl + year_month + "/" + name
        page_data = urlopen(url)
        json_object = load(page_data)
        return json_object

    def get_page_views_from_to(self, name, date_from, date_to):
        """Get page views from a wiki page with a specific name between two dates, ordered by the smallest date.

        The function expects the server response be in json and have the object daily_views.
        Also the daily_views has to have the key name be a date in the format of Y-m-d

        :param name:
        :param date_from:
        :param date_to:
        :return list:
        """

        final_dict = {}
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=date_from, until=date_to):
            json_objects = self.get_page_views_from_name_year_month(name, dt.strftime("%Y%m"))
            objects = json_objects['daily_views']
            for key, value in objects.iteritems():
                tmp_key = 0

                # check for exception, because non valid dates are given from the server
                try:
                    tmp_key = datetime.strptime(key, "%Y-%m-%d")
                except ValueError as e:
                    print "Invalid date " + key + " given to datetime: " + e.message

                if tmp_key != 0:
                    final_dict[tmp_key] = value

        return {k: v for k, v in final_dict.iteritems()}