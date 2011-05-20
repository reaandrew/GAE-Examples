from google.appengine.ext import db
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from google.appengine.api import users

from models import Forum,Thread,Post, Category
from forms import ForumForm,ThreadForm, PostForm, CategoryForm
from viewmodels import ForumCategoriesViewModel

from decorators import needs_login

class OpenIdUrl:
	def __init__(self, name, url):
		self.name = name
		self.url = url

@require_http_methods(["GET"])
def index(request):
	oProviders = [
		OpenIdUrl('Google', 'http://www.google.com/accounts/o8/id')
	]
	urls = []
	
	for provider in oProviders:
		urls.append(users.create_login_url("/", provider.name, provider.url))

	return render_to_response('home/index.html',{
			'viewmodel' : ForumCategoriesViewModel(),
			'urls' : urls,
			'logged_in' : users.get_current_user() is None
	})

@needs_login
@require_http_methods(["GET"])
def create_forum(request):
	return render_to_response('home/create_forum.html',
	{
		'forum_form' : ForumForm()
	})


@require_http_methods(["GET"])
def forum(request, forumid):
	forum = Forum.get_by_id(int(forumid))
	threads = Thread.all().filter('forum =',forum).order('-datetime').fetch(20)
	return render_to_response('home/forum.html',
	{
		'forum' : forum,
		'threads' : threads
	})

@require_http_methods(["GET"])
def thread(request, threadid):
	thread = Thread.get_by_id(int(threadid))
	posts = Post.all().filter('thread =', thread).order('datetime')
	
	return render_to_response('home/thread.html',
	{
		'forum' : thread.forum,
		'thread' : thread,
		'posts' : posts,
		'post_form' : PostForm()
	})

@require_http_methods(["GET"])
def create_thread(request, forumid):
	forum = Forum.get_by_id(int(forumid))
	
	return render_to_response('home/create_thread.html',
	{
		'forum' : forum,
		'thread_form' : ThreadForm()
	})

@needs_login
@require_http_methods(["POST"])
def create_forum_submit(request):
	forum = Forum(user = request._user, name="DEFAULT")
	
	data = ForumForm(request.POST, instance=forum)
	if data.is_valid():
		entity = data.save(commit=False)
		entity.put()
		return HttpResponseRedirect('/')
	
	return render_to_response('home/create_forum.html',
	{
		'forum_form' : data
	})


@needs_login
@require_http_methods(["POST"])
def create_thread_submit(request, forumid):
	forum = Forum.get_by_id(int(forumid))
	thread = Thread(forum=forum,user=request._user, content="Default", title="Default")
	data = ThreadForm(request.POST, instance=thread)
	if data.is_valid():
		entity = data.save(commit=False)
		entity.put()
		forum.increment_thread_count()
		forum.set_last_thread(entity)
		return HttpResponseRedirect('/forum/{0}'.format(forum.key().id()))

	return render_to_response('home/create_thread.html',
	{
		'thread_form' : data
	})



@needs_login
@require_http_methods(["POST"])
def create_post_submit(request, threadid):
	thread = Thread.get_by_id(int(threadid))
	#I have to add some value that is not null or empty to content
	#to get round what seems to be a bug with either Django forms or Django
	#forms with the google app engine
	post = Post(user=request._user, thread=thread, content="CONTENT")
	data = PostForm(data=request.POST, instance=post) 

	if data.is_valid():
		entity = data.save(commit=False)
		entity.put()
		return HttpResponseRedirect('/thread/{0}'.format(thread.key().id()))
	
	posts = Post.all().filter('thread =', thread).order('datetime')
	return render_to_response('home/thread.html',{
		'forum' : thread.forum,
		'thread' : thread,
		'posts' : posts,
		'post_form' : data
	})


	
@needs_login
@require_http_methods(["GET"])
def create_category(request):
	return render_to_response('home/create_category.html',
	{
		'category_form' : CategoryForm()
	})

@needs_login
@require_http_methods(["POST"])
def create_category_submit(request):
	category = Category(user=request._user, name="DEFAULT")
	data = CategoryForm(data=request.POST, instance=category)
	
	if data.is_valid():
		entity = data.save(commit=False)
		entity.put()
		return HttpResponseRedirect("/")

	return render_to_response('home/create_category.html',
	{
		'category_form' : data 
	})

