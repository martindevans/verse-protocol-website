import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import search

application = webapp.WSGIApplication([('/tasks/searchindexing', search.SearchIndexing)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
