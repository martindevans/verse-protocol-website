import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache

class MainPage(webapp.RequestHandler):
  def get(self):
##    stats = memcache.get_stats()
##    template_values = {
##      'hits': stats['hits'],
##      'misses': stats['misses'],
##      'byte_hits': stats['byte_hits'],
##      'items': stats['items'],
##      'bytes': stats['bytes'],
##      'oldest_item_age': stats['oldest_item_age']
##      }
##
##    path = os.path.join(os.path.dirname(__file__), 'djangoTemplates/adminpanel.html')
##    self.response.out.write(template.render(path, template_values))
    self.response.out.write("Admin panel")

application = webapp.WSGIApplication(
                                     [('/admin', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
