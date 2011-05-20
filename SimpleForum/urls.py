from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	(r'^$', 'views.index'),
	(r'^forums/$', 'views.index'),
	(r'^forum/(?P<forumid>\d+)/$', 'views.forum'),
	(r'^thread/(?P<threadid>\d+)/$', 'views.thread'),
	(r'^forum/create/$', 'views.create_forum'),
	(r'^forum/createsubmit/$', 'views.create_forum_submit'),
	(r'^forum/(?P<forumid>\d+)/createthread/$', 'views.create_thread'),
	(r'^forum/(?P<forumid>\d+)/createthreadsubmit/$', 'views.create_thread_submit'),
	(r'^thread/(?P<threadid>\d+)/createpostsubmit/$', 'views.create_post_submit'),
	(r'^category/create/$', 'views.create_category'),
	(r'^category/createsubmit/$', 'views.create_category_submit'),
	
	
	
	
    # url(r'^forum/', include('forum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
