import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from baselibrary import search

class AdminPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("Admin panel")

application = webapp.WSGIApplication([
                                    ('/admin.*', AdminPage),
                                    ('/tasks/searchindexing', search.SearchIndexing)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
