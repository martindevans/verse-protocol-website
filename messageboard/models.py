from google.appengine.ext import db
from google.appengine.api import users

import sys
sys.path.append("./customisation")
from customisation import config

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

    def GetPath(self):
        return '<a href="/messageboard/section?&sectionkey=' + str(self.key()) + '">' + self.title + '</a> &gt; '

    def GetCompletePath(self):
        return '<a href="/messageboard">' + config.values["appname"] + '</a> &gt; ' + self.GetPath()

class Thread(db.Model):
    parentSection = db.ReferenceProperty(section)
    title = db.StringProperty()
    readgroups = db.ListProperty(db.Key)
    writegroups = db.ListProperty(db.Key)
    datecreated = db.DateTimeProperty(auto_now_add=True)
    dateupdated = db.DateTimeProperty(auto_now=True)
    postcount = db.IntegerProperty()

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

    def GetPath(self):
        return '<a href="/messageboard/thread?&threadkey=' + str(self.key()) + '">' + self.title + '</a> &gt; '

    def GetCompletePath(self):
        return self.parentSection.GetCompletePath() + self.GetPath()

    def GetCompletePathWithPages(self, pageIndex, pageSize):
        return self.GetCompletePath() + self.GetPagePath(pageIndex, pageSize)

    def GetPagePath(self, pageIndex, pageSize):
        def gen(n, pageIndex):
            if (n == pageIndex):
                return str(n)
            else:
                return '<a href="/messageboard/thread?&threadkey=' + str(self.key()) + '&pageindex=' + str(n) + '">' + str(n) + '</a>'
        return ','.join(
            [gen(n, pageIndex) for n in range(1, self.GetPageCount(pageSize) + 1)])

    def GetNextPosition(self):
        def txn():
            if (self.postcount is None):
                self.postcount = 0
            self.postcount = self.postcount + 1
            self.put()
            return self.postcount - 1
        return db.run_in_transaction(txn)

    def GetPage(self, pageIndex, pageSize):
        return None

    def GetPageCount(self, pageSize):
        postCount = self.GetCount()
        fullPages = int(postCount / pageSize)
        if (postCount == fullPages * pageSize):
            return fullPages
        return fullPages + 1 #partial page

    def GetCount(self):
        return int(self.postcount - 1)

class Post(search.Searchable, db.Model):
    parentThread = db.ReferenceProperty(Thread)
    user = db.UserProperty(auto_current_user_add=True)
    datecreated = db.DateTimeProperty(auto_now_add=True)
    dateupdated = db.DateTimeProperty(auto_now=True)
    content = db.TextProperty()
    title = db.StringProperty()
    position = db.IntegerProperty()
    writes = db.IntegerProperty()
    groups = db.ListProperty(db.Key)
    INDEX_ONLY = ['content']  

    def put(self):
        if (self.writes is None):
            self.writes = 0
        self.writes = self.writes + 1
        db.put(self)

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
