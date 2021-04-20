import os
import re
import warnings
import importlib
from forum.models import UserAccount, Category, Hack, Comment
from populate import populate
from django.urls import reverse, resolve
from django.test import TestCase
from django.conf import settings
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.forms import fields as django_fields
from django.test import Client


HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}LifeHackForum => TEST FAILURE {os.linesep}================{os.linesep}"
FOOTER = f"{os.linesep}"

def create_user_object():
	user = User.objects.get_or_create(
	username='test',
	first_name='first_name',
	last_name='last_name',
	email='test@test.com')[0]
	
	user.set_password('testuser')
	user.save()
	return user

def create_super_user_object():
	return User.objects.create_superuser('admin', 'admin@admin.com', 'admin')

def get_template(path_to_template):
	t = open(path_to_template, 'r')
	templStr = ""

	for line in t:
		templStr = f"{templStr}{line}"

	t.close()
	return templStr


############################################# Set Up ###########################################################

class InitailTests(TestCase):
	def setUp(self):
		self.project_base_dir = os.getcwd()
		self.forum_app_dir = os.path.join(self.project_base_dir, 'forum')
	
	def test_project_created(self):
		has_directory = os.path.isdir(os.path.join(self.project_base_dir, 'forum'))
		has_urls = os.path.isfile(os.path.join(self.project_base_dir, 'forum', 'urls.py'))
		
		self.assertTrue(has_directory, f"{HEADER}configuration directory doesn't exist {FOOTER}")
		self.assertTrue(has_urls, f"{HEADER}urls.py module doesn't exist. {FOOTER}")
	
	def app_created(self):
		has_directory = os.path.isdir(self.forum_app_dir)
		is_python = os.path.isfile(os.path.join(self.forum_app_dir, '__init__.py'))
		has_views = os.path.isfile(os.path.join(self.forum_app_dir, 'views.py'))
		
		self.assertTrue(has_directory, f"{HEADER}The forum app directory doesn't exist.{FOOTER}")
		self.assertTrue(is_python, f"{HEADER}The directory missing files.{FOOTER}")
		self.assertTrue(has_views, f"{HEADER}The directory missing files. {FOOTER}")
	
	def has_urls_module(self):
		has_module = os.path.isfile(os.path.join(self.forum_app_dir, 'urls.py'))
		self.assertTrue(has_module, f"{HEADER}app's urls.py module missing.{FOOTER}")
		
############################################# Display hacks #########################################################

class HomePage(TestCase):

	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:home'))
		self.content = self.response.content.decode()
	
	def test_has_view(self):
		has_name = 'home' in self.views_module_listing
		is_callable = callable(self.views_module.home)
		
		self.assertTrue(has_name, f"{HEADER}The home() view for doesn't exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}The home() view not functioning.{FOOTER}")
	
	def test_has_mapping(self):
		home_has_mapping = False
		
		for mapping in self.urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'home':
					home_has_mapping = True
		
		self.assertTrue(home_has_mapping, f"{HEADER}The home URL mapping not found.{FOOTER}")
		self.assertEquals(reverse('forum:home'), '/forum/', f"{HEADER}The home URL lookup failed.{FOOTER}")
	

	def test_for_headder(self):
		response = self.client.get(reverse('forum:home'))
		quotes = '<h1>Top 3 Hacks of the Week</h1>' in response.content.decode()
		
		self.assertTrue(quotes, f"{HEADER}Header not in home page.{FOOTER}")

	
	def test_home_basics(self):
		self.assertTemplateUsed(self.response, 'forum/home.html', f"{HEADER}Your home() viewnot using correct template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}home.html template doesn't start with <!DOCTYPE html>{FOOTER}")
	
  
	def test_home_context_dictionary(self):
		expected_hacks = list(Hack.objects.order_by('-likes')[:3]) 
		self.assertTrue('hacks' in self.response.context, f"{HEADER}'hacks' variable not in context dictionary for the home() view. {FOOTER}")
		self.assertEqual(type(self.response.context['hacks']), QuerySet, f"{HEADER}The 'hacks' variable in the context dictionary for the home() view not a QuerySet.{FOOTER}")
		self.assertEqual(expected_hacks, list(self.response.context['hacks']), f"{HEADER}Incorrect hacks/hack order returned from the home() view context dictionary.{FOOTER}")

class Base1(TestCase):
	def test_base_template_exists(self):
 
		template_path = os.path.join(settings.TEMPLATE_DIR, 'forum', 'base1.html')
		self.assertTrue(os.path.exists(template_path), f"{HEADER}base1.html template not found {FOOTER}")
	
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
			self.assertTrue(lookup in template_str, f"{HEADER}in base1.html, hyperlink '{lookup}' not found. {FOOTER}")

class Base2(TestCase):
	def test_base_template_exists(self):
		template_path = os.path.join(settings.TEMPLATE_DIR, 'forum', 'base2.html')
		self.assertTrue(os.path.exists(template_path), f"{HEADER}We couldn't find the new base2.html template {FOOTER}")
	
	def test_template_usage(self):
		populate()
		
		urls = [reverse('forum:home'),
				reverse('forum:about'),]

		templates = ['forum/home.html',]
		
		for url, template in zip(urls, templates):
			response = self.client.get(url)
			self.assertTemplateUsed(response, template)

	def test_for_links_in_base(self):
		template_str = get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'base2.html'))

		look_for = [
			'<a href="{% url \'forum:about\' %}">About</a>',
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In base2.html, hyperlink '{lookup}' not found. {FOOTER}")				

class About(TestCase):
	
	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:about'))
		self.content = self.response.content.decode()
	
	def test_has_view(self):
		has_name = 'about' in self.views_module_listing
		is_callable = callable(self.views_module.about)
		
		self.assertTrue(has_name, f"{HEADER}The about() view for about doesn't exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}Check that you have created the about() view correctly. It doesn't seem to be a function!{FOOTER}")
	
	def test_has_mapping(self):
		about_mapping_exists = False
		
		for mapping in self.urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'about':
					about_mapping_exists = True
		
		self.assertTrue(about_mapping_exists, f"{HEADER}The about URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:about'), '/forum/about/', f"{HEADER}The about URL lookup failed.{FOOTER}")
	

	def test_about_basics(self):
		self.assertTemplateUsed(self.response, 'forum/about.html', f"{HEADER}Your about() view doesn't use the expected about.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your about.html template doesn't start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FOOTER}")
	
class CategoryP(TestCase):

	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:category', kwargs={'category_categoryName_slug': 'clothing'}))
		self.content = self.response.content.decode()
	
	def test_has_view(self):
		has_name = 'category' in self.views_module_listing
		is_callable = callable(self.views_module.category)
		
		self.assertTrue(has_name, f"{HEADER}category() view for doesn't exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}category() view not fucntioning{FOOTER}")
	
	
	def test_slug_functionality(self):

		category = Category.objects.get_or_create(
		categoryName='clothing', 
		description = 'dec',)[0]
		
		category.categoryName = "changed"
		category.save()

		self.assertEquals('changed', category.slug, f"{HEADER}When changing the name of a category. {FOOTER}")

	
	def test_has_mapping(self):
		category_mapping_exists = False
		
		for mapping in self.urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'category':
					category_mapping_exists = True
		
		self.assertTrue(category_mapping_exists, f"{HEADER}The category URL mapping not found.{FOOTER}")
		self.assertEquals(reverse('forum:category', kwargs={'category_categoryName_slug': 'clothing'}), '/forum/all_categories/clothing/', f"{HEADER}The category URL lookup failed.{FOOTER}")
	

	def test_category_basics(self):
		self.assertTemplateUsed(self.response, 'forum/category.html', f"{HEADER}Your category() view not using category.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your category.html template doesn't start with <!DOCTYPE html>.{FOOTER}")
	
  
	def test_category_context_dictionary(self):		
		category = Category.objects.get_or_create(
		categoryName='clothing', 
		description = 'dec',)[0]
		
		created_cat = Category.objects.get(categoryName = 'clothing')
		hack_list = list(Hack.objects.filter(categoryName=created_cat).order_by('-dateTimeCreated'))
		
		self.response = self.client.get(reverse('forum:category', kwargs={'category_categoryName_slug': 'clothing'}))
	 
		self.assertTrue('category' in self.response.context, f"{HEADER} 'category' not in context dictionary for the category() view.{FOOTER}")
		self.assertTrue('hacks' in self.response.context, f"{HEADER} 'hacks' variable not in context dictionary for the category() view.{FOOTER}")

		self.assertEqual(self.response.context['category'], created_cat, f"{HEADER}The category returned in the context dictionary for the category() incorrect . {FOOTER}")
		self.assertEqual(type(self.response.context['hacks']), QuerySet, f"{HEADER}The 'hacks' variable in the context dictionary for the category() view didn't return a QuerySet .{FOOTER}")
		self.assertEqual(list(self.response.context['hacks']), hack_list, f"{HEADER}The list of hacks returned in the context dictionary of the category() incorrect.{FOOTER}")
	
	
	def test_nonexistent(self):
		response = self.client.get(reverse('forum:category', kwargs={'category_categoryName_slug': 'nonexistent'}))
		lookup_string = 'The specified category does not exist.'
		self.assertIn(lookup_string, response.content.decode(), r"{HEADER}error message for empty category not found.{FOOTER}")
	
	def test_empty(self):
		category = Category.objects.get_or_create(
		categoryName='test', 
		description = 'dec',)[0]
		response = self.client.get(reverse('forum:category', kwargs={'category_categoryName_slug': 'test'}))
		lookup_string = '<strong>No hacks currently in category.</strong>'
		self.assertIn(lookup_string, response.content.decode(), r"{HEADER}error message for empty hacks not found{FOOTER}")
	
class AllCategories(TestCase):	
	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:all_categories'))
		self.content = self.response.content.decode()
	
	def test_has_view(self):
		has_name = 'all_categories' in self.views_module_listing
		is_callable = callable(self.views_module.all_categories)
		
		self.assertTrue(has_name, f"{HEADER}The all_categories() view for doesn't exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}all categories view not callable {FOOTER}")
	
	
	def test_has_mapping(self):
		category_mapping_exists = False
		
		for mapping in self.urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'all_categories':
					category_mapping_exists = True
		
		self.assertTrue(category_mapping_exists, f"{HEADER}The all_categories URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:all_categories'), '/forum/all_categories/', f"{HEADER}The category URL lookup failed.{FOOTER}")
	

	def test_allcategory_basics(self):
		self.assertTemplateUsed(self.response, 'forum/all_categories.html', f"{HEADER}Your all_categories() view doesn't use the expected category.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your all_categories.html template doesn't start with <!DOCTYPE html> {FOOTER}")
	
	def test_allcategory_context_dictionary(self):

		#create user object
		user = create_user_object()
		self.client.login(username='testuser', password='testuser')
		
		request = self.client.get(reverse('forum:all_categories'))
		content = request.content.decode('utf-8')
		
		#verified = QuerySet(False)
		category_list = list(Category.objects.order_by('categoryName'))

		self.response = self.client.get(reverse('forum:all_categories'))
		
		self.assertTrue('categories' in self.response.context , f"{HEADER}'category' variable in the context dictionary for all_category() view not found.{FOOTER}")
		self.assertTrue('verified' in self.response.context, f"{HEADER}'verified' variable in the context dictionary for all_category() view not found.{FOOTER}")
		
		#self.assertEqual(self.response.context['verified'], verified, f"{HEADER}The category returned in the context dictionary for the all_category() view did not match what was expected. {FOOTER}")
		self.assertEqual(type(self.response.context['categories']), QuerySet, f"{HEADER}The 'categories' variable in the context dictionary for the all_category()  not a QuerySet.{FOOTER}")
		self.assertEqual(list(self.response.context['categories']), category_list, f"{HEADER}categories returned in the context dictionary of all_category() view incorrect.{FOOTER}")
	
class HackP(TestCase):
	def setUp(self):
		populate()
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:hack', kwargs={'hack_hack_slug': '100', 'category_categoryName_slug' : 'liquid'}))
		self.content = self.response.content.decode()
	
	def test_has_view(self):
		has_name = 'hack' in self.views_module_listing
		is_callable = callable(self.views_module.hack)
		
		self.assertTrue(has_name, f"{HEADER}The hack() view for hack doesn't exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}hack view not callable.{FOOTER}")
	
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

		self.assertEquals("changed", hack.slug, f"{HEADER}slug didnt change after name change. {FOOTER}")

	
	def test_has_mapping(self):
		hack_mapping_exists = False
		
		for mapping in self.urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'hack':
					hack_mapping_exists = True
		
		self.assertTrue(hack_mapping_exists, f"{HEADER}The hack URL mapping could not be found.{FOOTER}")
		self.assertEquals(reverse('forum:hack', kwargs={'hack_hack_slug': '100', 'category_categoryName_slug' : 'liquid'}), '/forum/all_categories/liquid/100/', f"{HEADER}The hack URL lookup failed.{FOOTER}")
		self.assertEquals(reverse('forum:hack', kwargs={'hack_hack_slug': '100'}), '/forum/hack/100/', f"{HEADER}The hack URL lookup failed.{FOOTER}")
	

	def test_hack_basics(self):
		self.assertTemplateUsed(self.response, 'forum/hack.html', f"{HEADER}Your hack() view doesn't use the expected hack.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your hack.html template doesn't start with <!DOCTYPE html>{FOOTER}")
	
  
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
	 
		self.assertTrue('hack' in self.response.context, f"{HEADER}The 'hack' in context dictionary for the hack() view not found.{FOOTER}")
		self.assertTrue('comments' in self.response.context, f"{HEADER}The 'comments' in context dictionary for the hack() view not found.{FOOTER}")

		self.assertEqual(self.response.context['hack'], created_hack, f"{HEADER}The hack in context dictionary for the hack() incorrect. {FOOTER}")
		self.assertEqual(type(self.response.context['comments']), QuerySet, f"{HEADER}The 'comments' variable in context dictionary for hack() view not a  QuerySet.{FOOTER}")
		self.assertEqual(list(self.response.context['comments']), comment_list, f"{HEADER} comments returned in context dictionary of the hack() view incorrect .{FOOTER}")
	
	
	def test_nonexistent(self):
		response = self.client.get(reverse('forum:hack', kwargs={'hack_hack_slug': '100', 'category_categoryName_slug' : 'liquid'}))
		lookup_string = 'The specified hack does not exist.'
		self.assertIn(lookup_string, response.content.decode(), r"{HEADER}error message for non exsistant hack not found.{FOOTER}")
	
class AccountInfo(TestCase):

	def setUp(self):
		populate()
		newUser = create_user_object()
		account = UserAccount.objects.get_or_create(
		user=newUser)[0]
		self.client.login(username='test', password='testuser')
		self.views_module = importlib.import_module('forum.views')
		self.views_module_listing = dir(self.views_module)
		self.urls_module = importlib.import_module('forum.urls')
		self.response = self.client.get(reverse('forum:account_info', kwargs={'user_id_slug': 'test'}))
		self.content = self.response.content.decode()
	
	def test_has_view(self):
		has_name = 'account_info' in self.views_module_listing
		is_callable = callable(self.views_module.account_info)
		
		self.assertTrue(has_name, f"{HEADER}The account_info() view for account_info doesn't exist.{FOOTER}")
		self.assertTrue(is_callable, f"{HEADER}Check that you have created the account_info() view correctly. It doesn't seem to be a function!{FOOTER}")
	

	def test_has_mapping(self):
		account_info_mapping_exists = False
		
		for mapping in self.urls_module.urlpatterns:
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
		
		
		self.assertTemplateUsed(self.response, 'forum/account_info.html', f"{HEADER}Your account_info() view doesn't use the expected account_info.html template.{FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{HEADER}Your account_info.html template doesn't start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FOOTER}")
	
  
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
		 
		self.assertTrue('likes' in self.response.context, f"{HEADER}'likes' variable in context dictionary account_info() view not found. {FOOTER}")
		self.assertTrue('hacks' in self.response.context, f"{HEADER}'hacks' variable in the context dictionary for the account_info() view was not found.{FOOTER}")
		self.assertTrue('verified' in self.response.context, f"{HEADER}'verified' variable in the context dictionary for the account_info() view was not found.{FOOTER}")
		self.assertTrue('enoughlikes' in self.response.context, f"{HEADER}The 'enoughlikes' variable in the context dictionary for the account_info() view was not found.{FOOTER}")
		
		self.assertEqual(likesT, 500, f"{HEADER}The account_info() view is not returning expected number of likes {FOOTER}")
		
		self.assertEqual(type(self.response.context['hacks']), QuerySet, f"{HEADER}'hacks' variable in the context dictionary for the account_info() view not a QuerySet.{FOOTER}")
		self.assertEqual(list(self.response.context['hacks']), hack_list, f"{HEADER}hacks  in the context dictionary of the account_info() view incorrect. {FOOTER}")
	
############################################# Forms ###########################################################

#testing for forms is inaccissible due to logic partly in views

class CategoryFormClass(TestCase):
	def test_form_exists(self):
		project_path = os.getcwd()
		app_path = os.path.join(project_path, 'forum')
		module_path = os.path.join(app_path, 'forms.py')
		self.assertTrue(os.path.exists(module_path), f"{HEADER}Couldn't find forms.py module.{FOOTER}")

	def test_category_form_class(self):
		import forum.forms
		self.assertTrue('CategoryForm' in dir(forum.forms), f"{HEADER}The class CategoryForm could not in forms.py. {FOOTER}")

		from forum.forms import CategoryForm
		category_form = CategoryForm()

		self.assertEqual(type(category_form.__dict__['instance']), Category, f"{HEADER}The CategoryForm not linked Category model.{FOOTER}")

		fields = category_form.fields

		expected_fields = {
			'categoryName': django_fields.CharField,
			'description': django_fields.CharField,
			'slug': django_fields.CharField,
		}

		for expected_field_name in expected_fields:
			expected_field = expected_fields[expected_field_name]

			self.assertTrue(expected_field_name in fields.keys(), f"{HEADER}The field '{expected_field_name}' not in  CategoryForm{FOOTER}")
			self.assertEqual(expected_field, type(fields[expected_field_name]), f"{HEADER}The field '{expected_field_name}' in CategoryForm was not of the expected type '{type(fields[expected_field_name])}'.{FOOTER}")


	def test_add_category_url_mapping(self):
		try:
			resolved_name = resolve('/forum/all_categories/create_category/').view_name
		except:
			resolved_name = ''
		
		self.assertEqual(resolved_name, 'forum:create_category', f"{HEADER}The lookup '/forum/create_category/' didn't return mapping 'forum:create_category'.{FOOTER}")
	
	def test_for_link(self):
		template_str = get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'all_categories.html'))

		look_for = [
			 '<a href="{% url \'forum:create_category\' %}" id="create_category">'
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In create_category.html,'{lookup}', not found. {FOOTER}")

	def test_for_content(self):
		template_str = get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'create_category.html'))

		look_for = [
			 '<h1>Create a New Hacks.R.Us Category</h1>',
			 '<input type="text" name="categoryName" value="" size="50"/>',
			 '<input type="text" name="description" value="" size="50"/>',
			 '<input type="submit" value="Submit" />',
			 'action="{% url \'forum:create_category\'  %}"'
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In create_category.html, {lookup}' not found. {FOOTER}")

	def test_add_category_functionality(self):
		populate()
	
		ppost = self.client.post(reverse('forum:create_category'),{'categoryName': 'text', 'description':'description', 'shortDescription':'shortDescription'})
		
		self.assertEqual(ppost.status_code, 200, f"{HEADER}Error when adding new category, {FOOTER}")

class HackFormClass(TestCase):
	def test_form_exists(self):
		project_path = os.getcwd()
		app_path = os.path.join(project_path, 'forum')
		module_path = os.path.join(app_path, 'forms.py')
		self.assertTrue(os.path.exists(module_path), f"{HEADER}Couldn't find forms.py module.{FOOTER}")

	def test_hack_form_class(self):
		import forum.forms
		self.assertTrue('HackForm' in dir(forum.forms), f"{HEADER}The class HackForm could not in forms.py. {FOOTER}")

		from forum.forms import HackForm
		hack_form = HackForm()

		self.assertEqual(type(hack_form.__dict__['instance']), Hack, f"{HEADER}The HackForm not linked to Hack model.{FOOTER}")

		fields = hack_form.fields

		expected_fields = {
			'name' : django_fields.CharField,
			'shortDescription' : django_fields.CharField,
			'description' : django_fields.CharField,
			'image' : django_fields.ImageField,
			'dateTimeCreated' : django_fields.DateTimeField,
			'slug' : django_fields.SlugField,
		}

		for expected_field_name in expected_fields:
			expected_field = expected_fields[expected_field_name]

			self.assertTrue(expected_field_name in fields.keys(), f"{HEADER}The field '{expected_field_name}' not in HackForm .{FOOTER}")
			self.assertEqual(expected_field, type(fields[expected_field_name]), f"{HEADER}The field '{expected_field_name}' in HackForm was not of the expected type '{type(fields[expected_field_name])}'.{FOOTER}")


	def test_add_hack_url_mapping(self):
		try:
			resolved_name = resolve('/forum/all_categories/gaming/add_hack/').view_name
		except:
			resolved_name = ''
		
		self.assertEqual(resolved_name, 'forum:add_hack', f"{HEADER}lookup URL '/forum/add_hack/' didn't have mapping of 'forum:add_hack'.{FOOTER}")
	
	def test_for_link(self):
		template_str = get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'category.html'))

		look_for = [
			 '<a href="{% url \'forum:add_hack\' category.slug %}" id="addhack">'
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In category.html, '{lookup}', not found. {FOOTER}")

	def test_for_content(self):
		template_str = get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'add_hack.html'))

		look_for = [
			 '<h1>Create a new hack for {{context.category.categoryName}} </h1>',
			 '<label for="name"><b>Hack Name: </b></label>',
			 '<label for="shortDescription"><b>Short description </b></label>',
			 '<label for="description"><b>Describe the hack: </b></label>',
			 '<label for="image"><b>Add an image: </b></label>',
			 '<input type="submit" value="Submit" />',
			 '{% url \'forum:add_hack\' context.category.slug  %}'
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In add_hack.html,'{lookup}' not found. {FOOTER}")

	def test_add_hack_functionality(self):
		populate()
		
		category = Category.objects.get_or_create(
		categoryName='clothing', 
		description = 'dec',)[0]
		
		ppost = self.client.post('/forum/all_categories/clothing/add_hack/',{'name': 'testName', 'description':'test description', 'shortDescription':'short test'})
		
		#302 due to link changing
		self.assertEqual(ppost.status_code, 302, f"{HEADER}Error when adding new hack {FOOTER}")
			

class CommentFormClass(TestCase):
	def test_form_exists(self):
		project_path = os.getcwd()
		app_path = os.path.join(project_path, 'forum')
		module_path = os.path.join(app_path, 'forms.py')
		self.assertTrue(os.path.exists(module_path), f"{HEADER}Couldn't find forms.py module.{FOOTER}")

	def test_comment_form_class(self):
		import forum.forms
		self.assertTrue('CommentForm' in dir(forum.forms), f"{HEADER}The class CommentForm could not found in forum's forms.py. {FOOTER}")

		from forum.forms import CommentForm
		comment_form = CommentForm()

		self.assertEqual(type(comment_form.__dict__['instance']), Comment, f"{HEADER}The CommentForm doesn't link to the Comment model.{FOOTER}")

		fields = comment_form.fields

		expected_fields = {
			'text' : django_fields.CharField,
			'dateTimeCreated' : django_fields.DateTimeField,
		}

		for expected_field_name in expected_fields:
			expected_field = expected_fields[expected_field_name]

			self.assertTrue(expected_field_name in fields.keys(), f"{HEADER}The field '{expected_field_name}' not in CommentForm.{FOOTER}")
			self.assertEqual(expected_field, type(fields[expected_field_name]), f"{HEADER}The field '{expected_field_name}' in CommentForm was not of the expected type '{type(fields[expected_field_name])}'.{FOOTER}")


	def test_add_comment_url_mapping(self):
		try:
			resolved_name = resolve('/forum/water/add_comment/').view_name
		except:
			resolved_name = ''
		
		self.assertEqual(resolved_name, 'forum:add_comment', f"{HEADER}The lookup of URL '/forum/add_comment/' didn't return a mapping name of 'forum:add_comment'.{FOOTER}")
	
	def test_for_link(self):
		template_str = get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'hack.html'))

		look_for = [
			 '<form id="add_comment" method="post" action="{% url \'forum:add_comment\' hack.hackID %}">'
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In hack.html, we couldn't find the hyperlink '{lookup}'. {FOOTER}")

	def test_for_content(self):
		template_str = get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'hack.html'))

		look_for = [
			 ' <textarea name="text" id="new_comment"></textarea><br />',
			 ' <input type="button" id="checkComment" value="Submit" />',
			 ' <input type="submit" style="visibility: hidden" id="submitButton" value="Submit" />',
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{HEADER}In add_comment.html, we couldn't find the hyperlink '{lookup}'. {FOOTER}")

	def test_add_comment_functionality(self):
		populate()
		
		ppost = self.client.post('/forum/water/add_comment/',{'text': 'texting'})
		
		#302 due to link changing
		self.assertEqual(ppost.status_code, 302, f"{HEADER}Error when adding new comment, {FOOTER}")		


