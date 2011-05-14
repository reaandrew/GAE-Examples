from google.appengine.ext.db import djangoforms
from django import newforms as forms
from models import Forum, Thread, Post

class ForumForm(djangoforms.ModelForm):
	class Meta:
		model = Forum
		exclude = ['user']

class ThreadForm(djangoforms.ModelForm):
	class Meta:
		model = Thread
		exclude = ['user','forum']

class PostForm(djangoforms.ModelForm):
	class Meta:
		model = Post
		exclude = ['user','thread']

