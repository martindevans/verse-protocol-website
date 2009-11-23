import messageboard
from messageboard import admin

import sys
sys.path.append("./customisation")
from customisation import config

from messageboard import models
from messageboard.models import Thread

import cgi
import os

import google
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users

allowed_style_files = [
  "forumstyle.css",
  "menubottom.png",
  "menutop.png",
  "sectionliststyle.css",
  "threadliststyle.css",
  "createthreadstyle.css",
  "postliststyle.css",
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

    query = section.thread_set
    template_values = {
      "section" : section,
        }
    path = os.path.join(os.path.dirname(__file__), 'templates/' + "threadlist.html")
    self.response.out.write(RenderBaseExtender(path, template_values))

class Create(webapp.RequestHandler):
  def paramGet(self, defaultcontent, defaulttitle, key, reqType):
    template_values = {
      "parentkey" : key,
      "type" : reqType,
      "defaultcontent" : defaultcontent,
      "defaulttitle" : defaulttitle,
        }
    
    path = os.path.join(os.path.dirname(__file__), "templates/createform.html")
    self.response.out.write(RenderBaseExtender(path, template_values))
  
  def get(self):
    parentKey = self.request.get("parentkey")
    reqType = self.request.get("type")
    
    self.paramGet("", "", parentKey, reqType)

  def post(self):
    parentKey = self.request.get("parentkey")
    reqType = self.request.get("type")
    content = self.request.get("content")
    title = self.request.get("title")

    if (reqType == "thread" and title == ""):
      self.paramGet(content, title, parentKey, reqType)
      return

    #get a thread instance
    thread = None
    if (reqType == "thread"):
      thread = models.Thread()
      section = db.get(db.Key(parentKey))
      thread.parentSection = section
      thread.title = title
      thread.put()
    else:
      thread = models.Thread.get(db.Key(parentKey))

    #create a post instance
    post = models.Post()
    post.parentThread = thread
    post.content = content
    post.title = title
    post.put()
    post.enqueue_indexing(url='/tasks/searchindexing')  

    self.redirect("/messageboard/thread?&threadkey=" + str(thread.key()))

class PostList(webapp.RequestHandler):
  def get(self):
    thread = db.get(db.Key(self.request.get("threadkey")))

    template_values = {
      "thread" : thread,
        }
    path = os.path.join(os.path.dirname(__file__), "templates/postlist.html")
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
                                      ('/messageboard/section.*', ThreadList),
                                      ('/messageboard/create.*', Create),
                                      ('/messageboard/thread.*', PostList),
                                      ('/messageboard/admin.*', admin.AdminRoot),
                                       ('/.*', SectionList)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
