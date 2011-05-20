from google.appengine.ext.db import djangoforms
from django import newforms as forms
from models import Forum, Thread, Post, Category

class ForumForm(djangoforms.ModelForm):
	class Meta:
		model = Forum
		exclude = ['user','threadcount']

class ThreadForm(djangoforms.ModelForm):
	class Meta:
		model = Thread
		exclude = ['user','forum','postcount']

class PostForm(djangoforms.ModelForm):
	class Meta:
		model = Post
		exclude = ['user','thread']

class CategoryForm(djangoforms.ModelForm):
	class Meta:
		model = Category
		exclude = ['user']


