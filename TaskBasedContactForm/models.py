from google.appengine.ext import db

class Enquiry(db.Model):
	name = db.StringProperty()
	email = db.EmailProperty()
	telephone = db.PhoneNumberProperty()
	enquiry = db.StringProperty()



