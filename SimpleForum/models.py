from google.appengine.ext import db
from datetime import datetime

class BaseModel(db.Model):
	datetime = db.DateTimeProperty(auto_now_add=True) 

class Forum(BaseModel):
	name = db.StringProperty(required=True)
	user = db.UserProperty(required=True)

class Thread(BaseModel):
	title = db.StringProperty(required=True)
	content = db.StringProperty(multiline=True,required=True)
	user = db.UserProperty(required=True)
	forum = db.ReferenceProperty(Forum, required=True)

class Post(BaseModel):
	content = db.StringProperty(multiline=True,required=True)
	user = db.UserProperty()
	thread = db.ReferenceProperty(Thread)




