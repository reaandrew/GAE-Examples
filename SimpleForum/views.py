from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from google.appengine.api import users

from models import Forum
from forms import ForumForm

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
		'forums' : Forum.all().order('-datetime').fetch(10,offset=0),
		'urls' : urls,
		'logged_in' : users.get_current_user() is None
	})

@require_http_methods(["GET"])
def create_forum(request):
	return render_to_response('home/create_forum.html',
	{
		'forum_form' : ForumForm()
	})


'''
@require_http_methods(["GET"])
def forum(request, forumid):
	return render_to_response('home/forum.html')

@require_http_methods(["GET"])
def thread(request, threadid):
	return render_to_response('home/thread.html')

@require_http_methods(["GET"])
def create_thread(request, forumid):
	return render_to_response('home/create_thread.html')
'''

@require_http_methods(["POST"])
def create_forum_submit(request):
	data = ForumForm(request.POST)

	if data.is_valid():
		entity = data.save(commit=False)
		entity.user = users.get_current_user()
		entity.put()
		return HttpResponseRedirect('/')
	
	return render_to_response('home/create_forum.html',
	{
		'forum_form' : data
	})
'''
@require_http_methods(["POST"])
def create_thread_submit(request, forumid):
	return HttpResponseRedirect('/forum/1')

@require_http_methods(["POST"])
def create_post_submit(request, threadid):
	return HttpResponseRedirect('/thread/1')

@require_http_methods(["POST"])
def create_forum_handler(request):
	return HttpResponseRedirect('/forums/')

@require_http_methods(["POST"])
def create_thread_handler(request):
	return HttpResponseRedirect('/forum/1')

@require_http_methods(["POST"])
def create_post_handler(request):
	return HttpResponseRedirect('/thread/1')

@require_http_methods(["GET"])
def enquiry(request):
	return render_to_response('home/enquiry.html',
	{
		'enquiryform' : EnquiryForm()
	})

@require_http_methods(["GET"])
def enquiry_thanks(request):
	return render_to_response('home/enquiry_thanks.html')

@require_http_methods(["POST"])
def enquiry_submit(request):
	data  = EnquiryForm(request.POST)
	
	if data.is_valid():
		entity = data.save(commit=False)
		entity.put()
		return HttpResponseRedirect('/enquiry_thanks/')
	
	return render_to_response('home/enquiry.html',
	{
		'enquiryform' : form
	})
'''
