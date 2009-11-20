from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache

class UserProfile(db.Model):
  user = db.UserProperty()
  alias = db.StringProperty()

  def IsMemberOf(self, group):
    memberships = usersystem.groups.Membership.all().filter("profile = ", self)
    return memberships.count(1) != 0

def GetProfileFromUser(user):
  return get_or_insert(str(users.get_current_user().user_id(), user=user, alias=user.nickname()))
