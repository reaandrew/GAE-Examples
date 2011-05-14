from google.appengine.ext import db
from datetime import datetime

class BaseModel(db.Model):
	datetime = db.DateTimeProperty(auto_now_add=True) 

class Forum(BaseModel):
	name = db.StringProperty()
	user = db.UserProperty()

class Thread(BaseModel):
	title = db.StringProperty()
	content = db.StringProperty()
	user = db.UserProperty()
	forum = db.ReferenceProperty(Forum)

class Post(BaseModel):
	content = db.StringProperty()
	user = db.UserProperty()
	thread = db.ReferenceProperty(Thread)




