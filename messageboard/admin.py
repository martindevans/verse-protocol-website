from google.appengine.ext import webapp

import messageboard

class AdminRoot(webapp.RequestHandler):
  def get(self):
    self.response.out.write("Messageboard admin panel")
