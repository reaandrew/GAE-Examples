from models import Forum, Category, Thread,Post
import urllib, hashlib
import markdown

class ForumViewModel:

	def __init__(self, forum):
		self.model = forum
		self.lastthread = forum.get_last_thread()
		self.threadcount = forum.get_thread_count()
		self.postcount = forum.get_post_count()

class ForumCategoriesViewModel:
	
	def __init__(self):
		self.categories = []
		categories = Category.all()

		for category in categories:
			self.categories.append(ForumCategoryViewModel(category,ForumsViewModel(category)))

class ForumCategoryViewModel:

	def __init__(self, category, forumsviewmodel):
		self.category = category
		self.forums = forumsviewmodel.forums

class ForumsViewModel:

	def __init__(self, category):
		self.forums = []
		forums = Forum.all().filter('category =',category).order('-datetime').fetch(10, offset=0)
		for forum in forums:
			self.forums.append(ForumViewModel(forum))

class ThreadsViewModel:
	
	def __init__(self, forum):
		self.threads = []
		threads = Thread.all().filter('forum =',forum).order('-datetime').fetch(10,offset=0)
		for thread in threads:
			self.threads.append(ThreadViewModel(thread))

class ThreadViewModel:

	def __init__(self, thread):
		md = markdown.Markdown()
		self.title = thread.title
		self.lastpost = thread.get_last_post()
		self.postcount = thread.get_post_count()
		self.emailhash = hashlib.md5(thread.user.email().lower()).hexdigest()
		self.content = md.convert(thread.content)
		self.user = thread.user
		self.datetime = thread.datetime
		self.key = thread.key

class ThreadPostsViewModel:

	def __init__(self, thread):
		self.posts = []
		for post in Post.all().filter('thread =',thread).order('datetime'):
			self.posts.append(PostViewModel(post))
		
class PostViewModel:

	def __init__(self, post):
		md = markdown.Markdown()
		self.content = md.convert(post.content)
		self.emailhash = hashlib.md5(post.user.email().lower()).hexdigest()
		self.displayname = post.user.nickname()
		self.datetime = post.datetime
		
