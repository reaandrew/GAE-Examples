import logging, logging.handlers
from google.appengine.ext import db
from datetime import datetime
from google.appengine.api import memcache
import countersharding

class BaseModel(db.Model):
	datetime = db.DateTimeProperty(auto_now_add=True) 

	def __str__(self):
		return str(self.key())

class Category(BaseModel):
	name = db.StringProperty(required=True)
	user = db.UserProperty()
	def __str__(self):
		return self.name

class Forum(BaseModel):
	name = db.StringProperty(required=True)
	description = db.StringProperty(multiline=True)
	user = db.UserProperty(required=True)
	category = db.ReferenceProperty(Category,collection_name='forums')
	
	def get_last_thread(self):
		key = '{0}_lastthread'.format(self.key())
		lastthread = memcache.get(key)
		if lastthread is None:
			lastthread = Thread.all().filter('forum =',self).order('-datetime').get()
		memcache.set(key,lastthread)	
		return lastthread

	def set_last_thread(self, thread):
		key = '{0}_lastthread'.format(self.key())
		memcache.set(key, thread)

	def increment_thread_count(self):
		countersharding.increment('{0}_threadcount'.format(self.key()))

	def get_thread_count(self):
		return countersharding.get_count('{0}_threadcount'.format(self.key()))

	def increment_post_count(self):
		logging.info("forum post increment {0}".format(self.get_post_count()))
		countersharding.increment('{0}_postcount'.format(self.key()))

	def get_post_count(self):
		return countersharding.get_count('{0}_postcount'.format(self.key()))

class Thread(BaseModel):
	title = db.StringProperty(required=True)
	content = db.StringProperty(multiline=True,required=True)
	user = db.UserProperty(required=True)
	forum = db.ReferenceProperty(Forum, required=True)

	def get_last_post(self):
		key = '{0}_lastpost'.format(self.key())
		lastpost = memcache.get(key)
		if lastpost is None:
			lastpost = Post.all().filter('thread =',self).order('-datetime').get()
		memcache.set(key,lastpost)
		return lastpost

	def set_last_post(self,post):
		key = '{0}_lastpost'.format(self.key())
		memcache.set(key,post)

	def increment_post_count(self):
		logging.info("thread post increment {0}".format(self.get_post_count()))
		countersharding.increment(str(self.key()))

	def get_post_count(self):
		return countersharding.get_count(str(self.key()))

class Post(BaseModel):
	content = db.StringProperty(multiline=True,required=True)
	user = db.UserProperty()
	thread = db.ReferenceProperty(Thread)







