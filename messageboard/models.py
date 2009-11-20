from google.appengine.ext import db
from google.appengine.api import users

from usersystem import groups
from usersystem import profiles
from baselibrary import counter

class section(db.Model):
    title = db.StringProperty()
    groups = db.ListProperty(db.Key)

    def MayView(self, profile):
        for g in self.groups:
            if (profile.IsMemberOf(g)):
                return True
        return False

class Thread(db.Model):
    ParentSection = db.ReferenceProperty(section)
    title = db.StringProperty()
    groups = db.ListProperty(db.Key)

    def MayView(self, profile):
        for g in self.groups:
            if (profile.IsMemberOf(g)):
                return ParentSection.MayView(profile)
        return False

    def GetNextPosition(self):
        return counter.increment("ForumThreadPositionCounter" + self.title)

class Post(db.Model):
    ParentThread = db.ReferenceProperty(Thread)
    user = db.UserProperty(auto_current_user_add=True)
    date = db.DateTimeProperty(auto_now_add=True)
    content = db.TextProperty()
    position = db.IntegerProperty()
    groups = db.ListProperty(db.Key)

    def MayView(self, profile):
        return ParentThread.MayView(profile)

    def CurrentMayView(self):
        return MayView(profiles.GetProfileFromUser(users.get_current_user()))

    def GetAllowedContent(self):
        if (self.CurrentMayView()):
            return self.content
        else:
            return "You are not authorised to view this content"
