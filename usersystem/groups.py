from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import mail

import usersystem
from usersystem import profiles

class UserGroup(db.Model):
  title = db.StringProperty()
  description = db.TextProperty()

class Membership(db.Model):
  profile = db.ReferenceProperty(profiles.UserProfile)
  group = db.ReferenceProperty(UserGroup)
  Active = db.BooleanProperty(False)

  def Activate(self):
    """Activate a membership and returns the previous value of activation"""
    return self.SetActivation(True)

  def Deactivate(self):
    """Deactivate a membership and returns the previous value of activation"""
    return self.SetActivation(False)

  def SetActivation(self, value):
    """Sets activation of a membership and returns the previous value of activation"""
    def txn():
      previous = self.Active
      if (value != self.Active):
        self.Active = True
        self.put()
      return previous
    previous = db.run_in_transaction(txn)
    if (previous != value):
      bodycontent = ""
      if (value):
        bodycontent = "active"
      else:
        bodycontent = "disabled"
      mail.send_mail(sender=customisation.config.values["adminmail"],
                       to=self.profile.user.email(),
                       subject="User group notification",
                       body="""
  To """ + self.profile.user.nickname() + """
  This is to inform you that your membership to the group \"""" +
                     self.group.title + """\" at """ +
                     customisation.config.values["appname"] +
                     """is now """ +
                     bodycontent +
                     """

  Thanks,
  """ + customisation.config.values["appname"])
    return previous
                     
                     
