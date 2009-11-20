import messageboard

import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users

class Page(webapp.RequestHandler):
  def get(self):
      self.response.out.write("Message board")

application = webapp.WSGIApplication(
                                     [('/.*', Page)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
