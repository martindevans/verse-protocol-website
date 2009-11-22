import messageboard
from messageboard import admin

import sys
sys.path.append("./customisation")
from customisation import config

from messageboard import models

import cgi
import os

import google
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users

class SectionList(webapp.RequestHandler):
  def get(self):
    template_values = {
      "sections" : models.section.all().order("position")
        }
    path = os.path.join(os.path.dirname(__file__), 'templates/' + "sectionlist.html")
    self.response.out.write(RenderBaseExtender(path, template_values))

  def post(self):
    if (users.is_current_user_admin):
      operation = self.request.get("type")
      if (operation == "create"):
        name = self.request.get("name")
        description = self.request.get("description")
        s = models.section()
        s.title = name
        s.description = description
        s.position = int(self.request.get("order"))
        s.put()
        self.get()
      else:
        if (operation == "delete"):
          self.response.out.write("Delete ")
          try:
            key = self.request.get("key")
            self.response.out.write(key + " ")
            s = db.get(db.Key(key))
            s.delete()
            self.get()
          except Exception, e:
            self.response.out.write("Exception:" + str(e))
    else:
      self.get()

  def delete(self):
    if (users.is_current_user_admin):
      try:
        key = self.request.get("key")
        s = db.get(db.key(key))
        s.delete()
        self.response.out.write("success")
      except e:
        self.response.out.write(str(e))
    else:
      self.response.out.write("Not allowed")

class ThreadList(webapp.RequestHandler):
  def get(self):
    section = db.get(db.Key(self.request.get("sectionkey")))

    template_values = {
      "section" : section
        }
    path = os.path.join(os.path.dirname(__file__), 'templates/' + "threadlist.html")
    self.response.out.write(RenderBaseExtender(path, template_values))


allowed_style_files = [
  "forumstyle.css",
  "menubottom.png",
  "menutop.png",
  "sectionliststyle.css"
  ]

class File(webapp.RequestHandler):
  def get(self):
    filename = self.request.path[20:len(self.request.path)]
    if (filename in allowed_style_files):
      path = os.path.dirname(__file__) + "/files/" + filename
      stream = open(path, "rb")
      self.response.headers["Content-Type"] = self.request.query_string
      self.response.out.write(stream.read())
      stream.close()
    else:
      self.error(404)
      self.response.out.write("File : " + filename + " not found")

class Search(webapp.RequestHandler):
  def get(self):
    phrase = self.request.get("searchbox")
    results = models.Post.search(phrase)
    
    template_values = {
      "pagetitle" : "Search",
      "searchphrase" : phrase,
      "results" : results,
      "resultcount" : results.count(1000),
        }
    
    path = os.path.join(os.path.dirname(__file__), "templates/search.html")
    self.response.out.write(RenderBaseExtender(path, template_values))

def RenderBaseExtender(path, template_values):
  user = users.get_current_user()
  if user:
    template_values["accounthref"] = users.create_logout_url("/messageboard")
    template_values["accountstring"] = "Sign out"
  else:
    template_values["accounthref"] = users.create_login_url("/messageboard")
    template_values["accountstring"] = "Sign in"
  template_values["users"] = google.appengine.api.users
  template_values.update(config.values)
  return template.render(path, template_values)

application = webapp.WSGIApplication(
                                     [('/messageboard/files.*', File),
                                      ('/messageboard/search.*', Search),
                                      ('/messageboard/threadlist.*', ThreadList),
                                      ('/messageboard/admin.*', admin.AdminRoot),
                                       ('/.*', SectionList)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
