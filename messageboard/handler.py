import messageboard

import sys
sys.path.append("./customisation")
from customisation import config

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
    template_values = {
      "pagetitle" : "Title",
        }
    path = os.path.join(os.path.dirname(__file__), 'templates/' + "base.html")
    self.response.out.write(RenderBaseExtender(path, template_values))

allowed_style_files = [
  "forumstyle.css",
  "menubottom.png",
  "menutop.png",
  ]

class Style(webapp.RequestHandler):
  def get(self):
    filename = self.request.path[20:len(self.request.path)]
    if (filename in allowed_style_files):
      path = os.path.dirname(__file__) + "/files/" + filename
      stream = open(path, "rb")
      self.response.headers["Content-Type"] = self.request.query_string
      self.response.out.write(stream.read())
    else:
      self.error(404)
      self.response.out.write("File : " + filename + " not found")

def RenderBaseExtender(path, template_values):
  user = users.get_current_user()
  if user:
    template_values["accounthref"] = users.create_logout_url("/")
    template_values["accountstring"] = "Sign out"
  else:
    template_values["accounthref"] = users.create_login_url("/")
    template_values["accountstring"] = "Sign in"
  template_values.update(config.values)
  return template.render(path, template_values)

application = webapp.WSGIApplication(
                                     [('/messageboard/files.*', Style),
                                       ('/.*', Page)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
