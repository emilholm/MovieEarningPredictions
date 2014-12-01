__author__ = 'Martin Skytte'

import cherrypy
from webbrowser import open as wbopen
from simplejson import dumps
import os
from WikiSimpleAPIFunctions import WikiSimpleAPIFunctions
from BoxOfficeMojo import BoxOfficeMojo
from WikiPageViews import WikiPageViews
from YouTube import YouTube
from optparse import OptionParser

WEB_DIR = os.path.join(os.path.abspath("."), u"web")


class WebApp(object):

    def __init__(self):
        """
        Initiate the classes used in the web page.
        :return:
        """
        self.wikipageviews = WikiPageViews()
        self.boxofficemojo = BoxOfficeMojo()
        self.wikifunctions = WikiSimpleAPIFunctions()
        self.youtube = YouTube('AIzaSyDQ6enre5eE7f_BIegK-2MOBbBAlMWaJgI')

    @cherrypy.expose
    def index(self):
        """
        Expose the index html file on the server.
        :return html file:
        """

        return file(os.path.join(WEB_DIR, u'index.html'))

    @cherrypy.expose
    def searchwiki(self, movie):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dumps(self.wikifunctions.search_suggestions(movie))

    @cherrypy.expose
    def searchboxofficemojo(self, movie):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dumps(self.boxofficemojo.get_search_results(movie))

    @cherrypy.expose
    def searchyoutubetrailer(self, movie):
        title = movie.encode('utf-8')
        result = self.youtube.youtube_search(title, results=10)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dumps(result)

    @cherrypy.expose
    def getwikipageviews(self, wikiname, boxofficemojoname):
        wiki_name = wikiname.encode('utf-8')
        box_name = boxofficemojoname.encode('utf-8')
        created_date = self.wikifunctions.page_created_date(wiki_name)
        release_date = self.boxofficemojo.get_release_date(box_name)
        page_views = self.wikipageviews.get_page_views_from_to_by_monthly(wiki_name, created_date, release_date)
        result = {str(key): value for key, value in sorted(page_views.iteritems())}
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dumps(result)

    @cherrypy.expose
    def getfirstsevendaysearnings(self, boxofficemojoname):
        box_name = boxofficemojoname.encode('utf-8')
        result = self.boxofficemojo.get_first_seven_days(box_name)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dumps(result)


def open_page():
    """
    Open web page in browser
    :return:
    """

    wbopen("http://127.0.0.1:8080/")


config = {'/web':
          {
              'tools.staticdir.on': True,
              'tools.staticdir.dir': WEB_DIR,
          }}


cherrypy.engine.subscribe('start', open_page)
cherrypy.tree.mount(WebApp(), "/", config=config)
cherrypy.engine.start()