import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users

valid_pages = {
      "/": "/home.html",
      "/what": "/whatisverse.html",
      "/projects": "/verseprojects.html",
      "/documentation": "/documentation.html",
      "/sites": "/versesites.html"
      }

class Page(webapp.RequestHandler):
  def get(self):
    try:
      path = valid_pages[self.request.path]
      template_values = {
        }
      path = os.path.join(os.path.dirname(__file__), 'pages' + path)
      self.response.out.write(RenderBaseExtender(path, template_values))
    except KeyError:
      self.error(404)
      self.response.out.write("Oh noes, a 404 error!")

def RenderBaseExtender(path, template_values):
  user = users.get_current_user()
  if user:
    template_values["accounthref"] = users.create_logout_url("/")
    template_values["accountstring"] = "Sign out"
  else:
    template_values["accounthref"] = users.create_login_url("/")
    template_values["accountstring"] = "Sign in"
  return template.render(path, template_values)

application = webapp.WSGIApplication(
                                     [('/.*', Page)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
