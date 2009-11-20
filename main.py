import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users

class MainPage(webapp.RequestHandler):
  def get(self):    
    template_values = {
        }
    path = os.path.join(os.path.dirname(__file__), 'djangoTemplates/home.html')
    self.response.out.write(RenderBaseExtender(path, template_values))

def RenderBaseExtender(path, template_values):
  user = users.get_current_user()
  if user:
    template_values["accounthref"] = users.create_logout_url("/")
    template_values["accountstring"] = "Sign out"
  else:
    template_values["accounthref"] = users.create_login_url("/")
    template_values["accountstring"] = "Sign in"
  return template.render(path, template_values)

def GetBaseTemplateValues():
  user = users.get_current_user()
  answer = {}
  if user:
    answer["accounthref"] = users.create_logout_url("/")
    answer["accountstring"] = "Sign out"
  else:
    answer["accounthref"] = users.create_login_url("/")
    answer["accountstring"] = "Sign in"
  return answer

application = webapp.WSGIApplication(
                                     [('/.*', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
