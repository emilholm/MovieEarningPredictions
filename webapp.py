__author__ = 'Martin Skytte'

import cherrypy
import webbrowser
import os

WEB_DIR = os.path.join(os.path.abspath("."), u"web")


class WebApp(object):
    @cherrypy.expose
    def index(self):
        return file(os.path.join(WEB_DIR, u'index.html'))


def open_page():
    webbrowser.open("http://127.0.0.1:8080/")


config = {'/web':
          {
              'tools.staticdir.on': True,
              'tools.staticdir.dir': WEB_DIR,
          }}


cherrypy.engine.subscribe('start', open_page)
cherrypy.tree.mount(WebApp(), "/", config=config)
cherrypy.engine.start()