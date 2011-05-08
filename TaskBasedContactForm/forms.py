from google.appengine.ext.db import djangoforms
from django import newforms as forms
from models import Enquiry

class EnquiryForm(djangoforms.ModelForm):
	class Meta:
		model = Enquiry

