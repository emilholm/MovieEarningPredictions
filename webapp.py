__author__ = 'Martin Skytte'

import cherrypy
from webbrowser import open as wbopen
from simplejson import dumps
from urllib2 import unquote
import os
from WikiSimpleAPIFunctions import WikiSimpleAPIFunctions
from BoxOfficeMojo import BoxOfficeMojo
from WikiPageViews import WikiPageViews

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
    def getwikipageviews(self, wikiname):
        name = wikiname.encode('utf-8')
        print wikiname
        created_date = self.wikifunctions.page_created_date(name)
        print created_date
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dumps(created_date)



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