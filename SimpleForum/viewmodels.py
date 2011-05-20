from models import Forum, Category

class ForumViewModel:

	def __init__(self, forum):
		self.model = forum
		self.lastthread = forum.get_last_thread()
		self.threadcount = forum.get_thread_count()

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
		
		
