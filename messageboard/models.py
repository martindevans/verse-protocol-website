from google.appengine.ext import db

class section(db.Model):
    title = db.StringProperty()

class Thread(db.Model):
    ParentSection = db.ReferenceProperty(section)
    title = db.StringProperty()

class Post(db.Model):
    ParentThread = db.ReferenceProperty(Thread)
    user = db.UserProperty(auto_current_user_add=True)
    date = db.DateTimeProperty(auto_now_add=True)
    content = db.TextProperty()
    position = db.IntegerProperty()
