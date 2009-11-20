import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("Admin panel")

application = webapp.WSGIApplication(
                                     [('/admin', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
