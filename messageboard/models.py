from google.appengine.ext import db
from google.appengine.api import users

from usersystem import groups
from usersystem import profiles
from baselibrary import counter
from baselibrary import search

class section(db.Model):
    title = db.StringProperty()
    description = db.TextProperty()
    readgroups = db.ListProperty(db.Key)
    writegroups = db.ListProperty(db.Key)
    position = db.IntegerProperty()

    def MayRead(self, profile):
        groups = groups.UserGroup.get(self.readgroups)
        for g in groups:
            if (profile.IsMemberOf(g)):
                return True
        return len(groups) != 0

    def MayWrite(self, profile):
        groups = groups.UserGroup.get(self.writegroups)
        for g in groups:
            if (profile.IsMemberOf(g)):
                return True
        return len(groups) != 0

class Thread(db.Model):
    ParentSection = db.ReferenceProperty(section)
    title = db.StringProperty()
    readgroups = db.ListProperty(db.Key)
    writegroups = db.ListProperty(db.Key)
    datecreated = db.DateTimeProperty(auto_now_add=True)
    dateupdated = db.DateTimeProperty(auto_now=True)

    def MayRead(self, profile):
        groups = groups.UserGroup.get(self.readgroups)
        for g in groups:
            if (profile.IsMemberOf(g)):
                return ParentSection.MayRead(profile)
        return len(groups) != 0

    def MayWrite(self, profile):
        groups = groups.UserGroup.get(self.writegroups)
        for g in groups:
            if (profile.IsMemberOf(g)):
                return ParentSection.MayWrite(profile)
        return len(groups) != 0

    def GetNextPosition(self):
        return counter.increment("ForumThreadPositionCounter" + self.title)

class Post(search.Searchable, db.Model):
    ParentThread = db.ReferenceProperty(Thread)
    user = db.UserProperty(auto_current_user_add=True)
    datecreated = db.DateTimeProperty(auto_now_add=True)
    dateupdated = db.DateTimeProperty(auto_now=True)
    content = db.TextProperty()
    position = db.IntegerProperty()
    groups = db.ListProperty(db.Key)
    INDEX_ONLY = ['content']  

    def MayRead(self, profile):
        return ParentThread.MayRead(profile)

    def MayWrite(self, profile):
        return ParentThread.MayWrite(profile)

    def CurrentMayView(self):
        return MayView(profiles.GetProfileFromUser(users.get_current_user()))

    def GetAllowedContent(self):
        if (self.CurrentMayView()):
            return self.content
        else:
            return "You are not authorised to view this content"
