import os
import re
import warnings
import importlib
from forum.models import UserAccount, Category, Hack, Comment
from populate import populate
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.forms import fields as django_fields


HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}LifeHackForum TEST FAILURE {os.linesep}================{os.linesep}"
FOOTER = f"{os.linesep}"


def create_user_object():
    user = User.objects.get_or_create(username='test',
                                      first_name='first_name',
                                      last_name='last_name',
                                      email='test@test.com')[0]
    user.set_password('testuser')
    user.save()
    return user

def create_super_user_object():
    return User.objects.create_superuser('admin', 'admin@admin.com', 'admin')

def get_template(path_to_template):
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str


############################################# Set Up ###########################################################

class SetUpTests(TestCase):
	def setUp(self):
		self.project_base_dir = os.getcwd()
		self.forum_app_dir = os.path.join(self.project_base_dir, 'forum')
	
	def test_project_created(self):
		directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'forum'))
		urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'forum', 'urls.py'))
		
		self.assertTrue(directory_exists, f"{HEADER}Your project configuration directory doesn't exist {FOOTER}")
		self.assertTrue(urls_module_exists, f"{HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FOOTER}")
	
	def app_created(self):
		directory_exists = os.path.isdir(self.forum_app_dir)
		is_python_package = os.path.isfile(os.path.join(self.forum_app_dir, '__init__.py'))
		views_module_exists = os.path.isfile(os.path.join(self.forum_app_dir, 'views.py'))
		
		self.assertTrue(directory_exists, f"{HEADER}The forum app directory does not exist.{FOOTER}")
		self.assertTrue(is_python_package, f"{HEADER}The forum directory is missing files.{FOOTER}")
		self.assertTrue(views_module_exists, f"{HEADER}The forum directory is missing files. {FOOTER}")
	
	def has_urls_module(self):
		module_exists = os.path.isfile(os.path.join(self.forum_app_dir, 'urls.py'))
		self.assertTrue(module_exists, f"{HEADER}The forum app's urls.py module is missing.{FOOTER}")
		


############################################# Display hacks #########################################################

class HomePage(TestCase):

	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.project_urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:home'))
		self.content = self.response.content.decode()
	
	def test_view_exists(self):
		name_exists = 'home' in self.views_module_listing
		is_callable = callable(self.views_module.home)
		
		self.assertTrue(name_exists, f"{HEADER}The home() view for home does not exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}Check that you have created the home() view correctly. It doesn't seem to be a function!{FOOTER}")
	
	def test_mappings_exists(self):
		home_mapping_exists = False
		
		for mapping in self.project_urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'home':
					home_mapping_exists = True
		
		self.assertTrue(home_mapping_exists, f"{HEADER}The home URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:home'), '/forum/', f"{HEADER}The home URL lookup failed.{FOOTER}")
	

	def test_for_hyperlinks(self):
		response = self.client.get(reverse('forum:home'))
		single_quotes_check = '<a href=\'/forum/about/\'>About</a>' in response.content.decode() or '<a href=\'/forum/about\'>About</a>' in response.content.decode() 
		double_quotes_check = '<a href="/forum/about/">About</a>' in response.content.decode() or '<a href="/forum/about">About</a>' in response.content.decode()
		
		self.assertTrue(single_quotes_check or double_quotes_check, f"{HEADER}We couldn't find the hyperlink to the /forum/about/ URL in your home page.{FOOTER}")

	
	def test_home_basics(self):
		self.assertTemplateUsed(self.response, 'forum/home.html', f"{HEADER}Your home() view does not use the expected home.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your home.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FOOTER}")
	
  
	def test_home_context_dictionary(self):
		expected_hacks_order = list(Hack.objects.order_by('-likes')[:3]) 
		self.assertTrue('hacks' in self.response.context, f"{HEADER}We couldn't find a 'hacks' variable in the context dictionary within the home() view. {FOOTER}")
		self.assertEqual(type(self.response.context['hacks']), QuerySet, f"{HEADER}The 'hacks' variable in the context dictionary for the home() view didn't return a QuerySet object as expected.{FOOTER}")
		self.assertEqual(expected_hacks_order, list(self.response.context['hacks']), f"{HEADER}Incorrect hacks/hack order returned from the home() view's context dictionary -- expected {expected_hacks_order}; got {list(self.response.context['hacks'])}.{FOOTER}")

class Base1(TestCase):
	def test_base_template_exists(self):
 
		template_base_path = os.path.join(settings.TEMPLATE_DIR, 'forum', 'base1.html')
		self.assertTrue(os.path.exists(template_base_path), f"{HEADER}We couldn't find the new base1.html template {FOOTER}")
	
	def test_template_usage(self):
		populate()
		
		urls = [reverse('forum:home'),
				reverse('forum:about'),
				reverse('forum:category', kwargs={'category_categoryName_slug': 'gaming'}),
				reverse('forum:all_categories',),]

		templates = ['forum/home.html',]
		
		for url, template in zip(urls, templates):
			response = self.client.get(url)
			self.assertTemplateUsed(response, template)

	def test_for_links_in_base(self):
		template_str = get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'base1.html'))

		look_for = [
			'<a href="{% url \'forum:all_categories\' %}">All Categories</a>',
			'<a href="{% url \'forum:about\' %}">About</a>',
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In base1.html, we couldn't find the hyperlink '{lookup}'. {FOOTER}")

class Base2(TestCase):
	def get_template(self, path_to_template):
		f = open(path_to_template, 'r')
		template_str = ""
		for line in f:
			template_str = f"{template_str}{line}"
		f.close()
		return template_str
	
	def test_base_template_exists(self):
 
		template_base_path = os.path.join(settings.TEMPLATE_DIR, 'forum', 'base2.html')
		self.assertTrue(os.path.exists(template_base_path), f"{HEADER}We couldn't find the new base2.html template {FOOTER}")
	
	def test_template_usage(self):
		populate()
		
		urls = [reverse('forum:home'),
				reverse('forum:about'),]

		templates = ['forum/home.html',]
		
		for url, template in zip(urls, templates):
			response = self.client.get(url)
			self.assertTemplateUsed(response, template)

	def test_for_links_in_base(self):
		template_str = self.get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'base2.html'))

		look_for = [
			'<a href="{% url \'forum:about\' %}">About</a>',
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In base2.html, we couldn't find the hyperlink '{lookup}'. {FOOTER}")				

class About(TestCase):
	
	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.project_urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:about'))
		self.content = self.response.content.decode()
	
	def test_view_exists(self):
		name_exists = 'about' in self.views_module_listing
		is_callable = callable(self.views_module.about)
		
		self.assertTrue(name_exists, f"{HEADER}The about() view for about does not exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}Check that you have created the about() view correctly. It doesn't seem to be a function!{FOOTER}")
	
	def test_mappings_exists(self):
		about_mapping_exists = False
		
		for mapping in self.project_urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'about':
					about_mapping_exists = True
		
		self.assertTrue(about_mapping_exists, f"{HEADER}The about URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:about'), '/forum/about/', f"{HEADER}The about URL lookup failed.{FOOTER}")
	

	def test_about_basics(self):
		self.assertTemplateUsed(self.response, 'forum/about.html', f"{HEADER}Your about() view does not use the expected about.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your about.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FOOTER}")
	
class CategoryP(TestCase):

	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.project_urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:category', kwargs={'category_categoryName_slug': 'clothing'}))
		self.content = self.response.content.decode()
	
	def test_view_exists(self):
		name_exists = 'category' in self.views_module_listing
		is_callable = callable(self.views_module.category)
		
		self.assertTrue(name_exists, f"{HEADER}The category() view for category does not exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}Check that you have created the category() view correctly. It doesn't seem to be a function!{FOOTER}")
	
	
	def test_slug_functionality(self):

		category = Category.objects.get_or_create(
		categoryName='clothing', 
		description = 'dec',)[0]
		
		category.categoryName = "changed"
		category.save()

		self.assertEquals('changed', category.slug, f"{HEADER}When changing the name of a category. {FOOTER}")

	
	def test_mappings_exists(self):
		category_mapping_exists = False
		
		for mapping in self.project_urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'category':
					category_mapping_exists = True
		
		self.assertTrue(category_mapping_exists, f"{HEADER}The category URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:category', kwargs={'category_categoryName_slug': 'clothing'}), '/forum/all_categories/clothing/', f"{HEADER}The category URL lookup failed.{FOOTER}")
	

	def test_category_basics(self):
		self.assertTemplateUsed(self.response, 'forum/category.html', f"{HEADER}Your category() view does not use the expected category.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your category.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FOOTER}")
	
  
	def test_category_context_dictionary(self):		
		category = Category.objects.get_or_create(
		categoryName='clothing', 
		description = 'dec',)[0]
		
		created_cat = Category.objects.get(categoryName = 'clothing')
		hack_list = list(Hack.objects.filter(categoryName=created_cat).order_by('-dateTimeCreated'))
		
		self.response = self.client.get(reverse('forum:category', kwargs={'category_categoryName_slug': 'clothing'}))
	 
		self.assertTrue('category' in self.response.context, f"{HEADER}The 'category' variable in the context dictionary for the category() view was not found. Did you spell it correctly?{FOOTER}")
		self.assertTrue('hacks' in self.response.context, f"{HEADER}The 'hacks' variable in the context dictionary for the category() view was not found.{FOOTER}")

		self.assertEqual(self.response.context['category'], created_cat, f"{HEADER}The category returned in the context dictionary for the category) view did not match what was expected. {FOOTER}")
		self.assertEqual(type(self.response.context['hacks']), QuerySet, f"{HEADER}The 'hacks' variable in the context dictionary for the category() view didn't return a QuerySet object as expected.{FOOTER}")
		self.assertEqual(list(self.response.context['hacks']), hack_list, f"{HEADER}The list of hacks returned in the context dictionary of the category() view was not correct.{FOOTER}")
	
	
	def test_nonexistent(self):
		response = self.client.get(reverse('forum:category', kwargs={'category_categoryName_slug': 'nonexistent'}))
		lookup_string = 'The specified category does not exist.'
		self.assertIn(lookup_string, response.content.decode(), r"{HEADER}The expected message when attempting to access a non-existent category was not found.{FOOTER}")
	
	def test_empty(self):
		category = Category.objects.get_or_create(
		categoryName='test', 
		description = 'dec',)[0]
		response = self.client.get(reverse('forum:category', kwargs={'category_categoryName_slug': 'test'}))
		lookup_string = '<strong>No hacks currently in category.</strong>'
		self.assertIn(lookup_string, response.content.decode(), r"{HEADER}The expected message when accessing a category without hacks was not found.{FOOTER}")
	
class AllCategories(TestCase):	
	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.project_urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:all_categories'))
		self.content = self.response.content.decode()
	
	def test_view_exists(self):
		name_exists = 'all_categories' in self.views_module_listing
		is_callable = callable(self.views_module.all_categories)
		
		self.assertTrue(name_exists, f"{HEADER}The all_categories() view for does not exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}Check that you have created the all_categories() view correctly.{FOOTER}")
	
	
	def test_mappings_exists(self):
		category_mapping_exists = False
		
		for mapping in self.project_urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'all_categories':
					category_mapping_exists = True
		
		self.assertTrue(category_mapping_exists, f"{HEADER}The all_categories URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:all_categories'), '/forum/all_categories/', f"{HEADER}The category URL lookup failed.{FOOTER}")
	

	def test_allcategory_basics(self):
		self.assertTemplateUsed(self.response, 'forum/all_categories.html', f"{HEADER}Your all_categories() view does not use the expected category.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your all_categories.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FOOTER}")
	
	def test_allcategory_context_dictionary(self):

		#create user object
		user = create_user_object()
		self.client.login(username='testuser', password='testuser')
		
		request = self.client.get(reverse('forum:all_categories'))
		content = request.content.decode('utf-8')
		
		#verified = QuerySet(False)
		category_list = list(Category.objects.order_by('categoryName'))

		self.response = self.client.get(reverse('forum:all_categories'))
		
		self.assertTrue('categories' in self.response.context , f"{HEADER}The 'category' variable in the context dictionary for the all_category() view was not found. Did you spell it correctly?{FOOTER}")
		self.assertTrue('verified' in self.response.context, f"{HEADER}The 'verified' variable in the context dictionary for the all_category() view was not found.{FOOTER}")
		
		#self.assertEqual(self.response.context['verified'], verified, f"{HEADER}The category returned in the context dictionary for the all_category() view did not match what was expected. {FOOTER}")
		self.assertEqual(type(self.response.context['categories']), QuerySet, f"{HEADER}The 'categories' variable in the context dictionary for the all_category() view didn't return a QuerySet object as expected.{FOOTER}")
		self.assertEqual(list(self.response.context['categories']), category_list, f"{HEADER}The list of categories returned in the context dictionary of the all_category() view was not correct.{FOOTER}")
	
class HackP(TestCase):
	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.project_urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:hack', kwargs={'hack_hack_slug': '100', 'category_categoryName_slug' : 'liquid'}))
		self.content = self.response.content.decode()
	
	def test_view_exists(self):
		name_exists = 'hack' in self.views_module_listing
		is_callable = callable(self.views_module.hack)
		
		self.assertTrue(name_exists, f"{HEADER}The hack() view for hack does not exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}Check that you have created the hack() view correctly.{FOOTER}")
	
	def test_slug_functionality(self):
		category = Category.objects.get_or_create(
		categoryName='liquid', 
		description = 'dec',)[0]
		
		hack = Hack.objects.get_or_create(
		name='water',
		description = 'dec',
		shortDescription = 'sdesc', 
		categoryName = category)[0]
		
		hack.name = "changed"
		hack.save()

		self.assertEquals("changed", hack.slug, f"{HEADER}When changing the name of a hack. {FOOTER}")

	
	def test_mappings_exists(self):
		hack_mapping_exists = False
		
		for mapping in self.project_urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'hack':
					hack_mapping_exists = True
		
		self.assertTrue(hack_mapping_exists, f"{HEADER}The hack URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:hack', kwargs={'hack_hack_slug': '100', 'category_categoryName_slug' : 'liquid'}), '/forum/all_categories/liquid/100/', f"{HEADER}The hack URL lookup failed.{FOOTER}")
		self.assertEquals(reverse('forum:hack', kwargs={'hack_hack_slug': '100'}), '/forum/hack/100/', f"{HEADER}The hack URL lookup failed.{FOOTER}")
	

	def test_hack_basics(self):
		self.assertTemplateUsed(self.response, 'forum/hack.html', f"{HEADER}Your hack() view does not use the expected hack.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your hack.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FOOTER}")
	
  
	def test_hack_context_dictionary(self):		
		category = Category.objects.get_or_create(
		categoryName='liquid', 
		description = 'dec',)[0]
		
		hack = Hack.objects.get_or_create(
		name='water',
		description = 'dec',
		shortDescription = 'sdesc', 
		categoryName = category)[0]
		
		slug = hack.slug
		created_hack = Hack.objects.get(name = 'water')
		comment_list = list(Comment.objects.filter(hackID = created_hack).order_by('-dateTimeCreated'))
		
		self.response = self.client.get(reverse('forum:hack', kwargs={'hack_hack_slug': 26, 'category_categoryName_slug' : 'liquid'}))
	 
		self.assertTrue('hack' in self.response.context, f"{HEADER}The 'hack' variable in the context dictionary for the hack() view was not found. Did you spell it correctly?{FOOTER}")
		self.assertTrue('comments' in self.response.context, f"{HEADER}The 'comments' variable in the context dictionary for the hack() view was not found.{FOOTER}")

		self.assertEqual(self.response.context['hack'], created_hack, f"{HEADER}The hack returned in the context dictionary for the hack) view did not match what was expected. {FOOTER}")
		self.assertEqual(type(self.response.context['comments']), QuerySet, f"{HEADER}The 'comments' variable in the context dictionary for the hack() view didn't return a QuerySet object as expected.{FOOTER}")
		self.assertEqual(list(self.response.context['comments']), comment_list, f"{HEADER}The list of comments returned in the context dictionary of the hack() view was not correct.{FOOTER}")
	
	
	def test_nonexistent(self):
		response = self.client.get(reverse('forum:hack', kwargs={'hack_hack_slug': '100', 'category_categoryName_slug' : 'liquid'}))
		lookup_string = 'The specified hack does not exist.'
		self.assertIn(lookup_string, response.content.decode(), r"{HEADER}The expected message when attempting to access a non-existent hack was not found.{FOOTER}")
	

class AccountInfo(TestCase):

	def setUp(self):
		populate()
		newUser = create_user_object()
		account = UserAccount.objects.get_or_create(
		user=newUser)[0]
		self.client.login(username='test', password='testuser')
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.project_urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:account_info', kwargs={'user_id_slug': 'test'}))
		self.content = self.response.content.decode()
	
	def test_view_exists(self):
		name_exists = 'account_info' in self.views_module_listing
		is_callable = callable(self.views_module.account_info)
		
		self.assertTrue(name_exists, f"{HEADER}The account_info() view for account_info does not exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}Check that you have created the account_info() view correctly. It doesn't seem to be a function!{FOOTER}")
	

	def test_mappings_exists(self):
		account_info_mapping_exists = False
		
		for mapping in self.project_urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'account_info':
					account_info_mapping_exists = True
		
		self.assertTrue(account_info_mapping_exists, f"{HEADER}The account_info URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:account_info', kwargs={'user_id_slug': 'test'}), '/forum/account_info/test/', f"{HEADER}The account_info URL lookup failed.{FOOTER}")
	

	def test_account_info_basics(self):
	
		newUser = create_user_object()
		account = UserAccount.objects.get_or_create(
		user=newUser)[0]
		self.client.login(username='test', password='testuser')
		
		
		self.assertTemplateUsed(self.response, 'forum/account_info.html', f"{HEADER}Your account_info() view does not use the expected account_info.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your account_info.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FOOTER}")
	
  
	def test_account_info_context_dictionary(self):	
		newUser = create_user_object()
		account = UserAccount.objects.get_or_create(
		user=newUser)[0]
		
		category = Category.objects.get_or_create(
		categoryName='big', 
		description = 'dec',)[0]
		
		hack = Hack.objects.get_or_create(
		name='large',
		description = 'dec',
		shortDescription = 'sdesc', 
		user = account,
		likes = 500,
		categoryName = category)[0]
		
		self.client.login(username='test', password='testuser')
	
		hack_list = list(Hack.objects.filter(user__user = account))
		likesT = Hack.objects.filter(user__user = account).aggregate(Sum('likes'))['likes__sum']
			
		self.response = self.client.get(reverse('forum:account_info', kwargs={'user_id_slug': 'test'}))
		 
		self.assertTrue('likes' in self.response.context, f"{HEADER}The 'likes' variable in the context dictionary for the account_info() view was not found. Did you spell it correctly?{FOOTER}")
		self.assertTrue('hacks' in self.response.context, f"{HEADER}The 'hacks' variable in the context dictionary for the account_info() view was not found.{FOOTER}")
		self.assertTrue('verified' in self.response.context, f"{HEADER}The 'verified' variable in the context dictionary for the account_info() view was not found. Did you spell it correctly?{FOOTER}")
		self.assertTrue('enoughlikes' in self.response.context, f"{HEADER}The 'enoughlikes' variable in the context dictionary for the account_info() view was not found. Did you spell it correctly?{FOOTER}")
		
		self.assertEqual(likesT, 500, f"{HEADER}The account_info() view is not returning expected number of likes {FOOTER}")
		
		self.assertEqual(type(self.response.context['hacks']), QuerySet, f"{HEADER}The 'hacks' variable in the context dictionary for the account_info() view didn't return a QuerySet object as expected.{FOOTER}")
		self.assertEqual(list(self.response.context['hacks']), hack_list, f"{HEADER}The list of hacks returned in the context dictionary of the account_info() view was not correct.{FOOTER}")
	
############################################# Forms ###########################################################



############################################# Populate ###########################################################




############################################# Models ###########################################################





############################################# Admin ###########################################################






############################################# Sighn In \ out ###########################################################

