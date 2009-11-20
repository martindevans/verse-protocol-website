from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache

class UserProfile(db.Model):
  userid = db.StringProperty()
  user = db.UserProperty()
  alias = db.StringProperty()
