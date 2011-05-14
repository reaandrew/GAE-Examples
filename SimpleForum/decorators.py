from google.appengine.api import users
from django.http import HttpResponseRedirect

'''
This was originally from
https://clipr.torchbox.com/128/

I have changed to work with Django and not the GAE Web Framework

'''
def needs_login(meth):
    """Method decorator to ensure login"""
    def secure(request, *a, **kw):
        request._user = users.get_current_user()
        if not request._user:
            return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
        return meth(request, *a, **kw)
	
    return secure
