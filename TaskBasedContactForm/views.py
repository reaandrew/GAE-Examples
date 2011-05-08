from google.appengine.api import taskqueue
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from forms import EnquiryForm
from models import Enquiry

@require_http_methods(["GET"])
def index(request):
	return render_to_response('home/index.html')

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
		taskqueue.add(url='/tasks/sendenquiry/', params=request.POST)
		return HttpResponseRedirect('/enquiry_thanks/')
	
	return render_to_response('home/enquiry.html',
	{
		'enquiryform' : form
	})

@require_http_methods(["POST"])
def enquiry_task_process(request):
	data  = EnquiryForm(request.POST)
	entity = data.save(commit=False)
	entity.put()
	return HttpResponse()






