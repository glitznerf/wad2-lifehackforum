import os
import re
import warnings
import importlib
from forum.models import *
from populate import populate
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.db.models.query import QuerySet

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


############################################# Pages #########################################################

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
		
		self.assertTrue(name_exists, f"{FAILURE_HEADER}The home() view for forum does not exist.{FAILURE_FOOTER}")
		self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the home() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")
	
	def test_mappings_exists(self):
		home_mapping_exists = False
		
		for mapping in self.project_urls_module.urlpatterns:
			if hasattr(mapping, 'name'):
				if mapping.name == 'home':
					home_mapping_exists = True
		
		self.assertTrue(home_mapping_exists, f"{FAILURE_HEADER}The home URL mapping could not be found.{FAILURE_FOOTER}")
		self.assertEquals(reverse('forum:home'), '/forum/', f"{FAILURE_HEADER}The home URL lookup failed.{FAILURE_FOOTER}")
	

	def test_for_hyperlinks(self):
		response = self.client.get(reverse('forum:home'))
		single_quotes_check = '<a href=\'/forum/about/\'>About</a>' in response.content.decode() or '<a href=\'/forum/about\'>About</a>' in response.content.decode() 
		double_quotes_check = '<a href="/forum/about/">About</a>' in response.content.decode() or '<a href="/forum/about">About</a>' in response.content.decode()
		
		self.assertTrue(single_quotes_check or double_quotes_check, f"{FAILURE_HEADER}We couldn't find the hyperlink to the /forum/about/ URL in your home page.{FAILURE_FOOTER}")

	
	def test_home_basics(self):
		self.assertTemplateUsed(self.response, 'forum/home.html', f"{FAILURE_HEADER}Your home() view does not use the expected home.html template.{FAILURE_FOOTER}")
		self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Your home.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")
	
  
	def test_home_context_dictionary(self):
		expected_hacks_order = list(Hack.objects.order_by('-likes')[:3]) 
		self.assertTrue('hacks' in self.response.context, f"{FAILURE_HEADER}We couldn't find a 'hacks' variable in the context dictionary within the home() view. {FAILURE_FOOTER}")
		self.assertEqual(type(self.response.context['hacks']), QuerySet, f"{FAILURE_HEADER}The 'hacks' variable in the context dictionary for the home() view didn't return a QuerySet object as expected.{FAILURE_FOOTER}")
		self.assertEqual(expected_hacks_order, list(self.response.context['hacks']), f"{FAILURE_HEADER}Incorrect hacks/hack order returned from the home() view's context dictionary -- expected {expected_hacks_order}; got {list(self.response.context['hacks'])}.{FAILURE_FOOTER}")

class Base1(TestCase):
	def get_template(self, path_to_template):
		f = open(path_to_template, 'r')
		template_str = ""
		for line in f:
			template_str = f"{template_str}{line}"
		f.close()
		return template_str
	
	def test_base_template_exists(self):
 
		template_base_path = os.path.join(settings.TEMPLATE_DIR, 'forum', 'base1.html')
		self.assertTrue(os.path.exists(template_base_path), f"{FAILURE_HEADER}We couldn't find the new base1.html template {FAILURE_FOOTER}")
	
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
		template_str = self.get_template(os.path.join(settings.TEMPLATE_DIR, 'forum', 'base1.html'))

		look_for = [
			'<a href="{% url \'forum:all_categories\' %}">All Categories</a>',
			'<a href="{% url \'forum:about\' %}">About</a>',
		]
		
		for lookup in look_for:
			self.assertTrue(lookup in template_str, f"{FAILURE_HEADER}In base1.html, we couldn't find the hyperlink '{lookup}'. {FAILURE_FOOTER}")

class base2(TestCase):
	def get_template(self, path_to_template):
		f = open(path_to_template, 'r')
		template_str = ""
		for line in f:
			template_str = f"{template_str}{line}"
		f.close()
		return template_str
	
	def test_base_template_exists(self):
 
		template_base_path = os.path.join(settings.TEMPLATE_DIR, 'forum', 'base2.html')
		self.assertTrue(os.path.exists(template_base_path), f"{FAILURE_HEADER}We couldn't find the new base2.html template {FAILURE_FOOTER}")
	
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
			self.assertTrue(lookup in template_str, f"{FAILURE_HEADER}In base2.html, we couldn't find the hyperlink '{lookup}'. {FAILURE_FOOTER}")				


############################################# Forms ###########################################################



############################################# Populate ###########################################################




############################################# Models ###########################################################




############################################# Set Up ###########################################################

class SetUpTests(TestCase):
	def setUp(self):
		self.project_base_dir = os.getcwd()
		self.forum_app_dir = os.path.join(self.project_base_dir, 'forum')
	
	def test_project_created(self):
		directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'forum'))
		urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'forum', 'urls.py'))
		
		self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project configuration directory doesn't exist {FAILURE_FOOTER}")
		self.assertTrue(urls_module_exists, f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")
	
	def app_created(self):
		directory_exists = os.path.isdir(self.forum_app_dir)
		is_python_package = os.path.isfile(os.path.join(self.forum_app_dir, '__init__.py'))
		views_module_exists = os.path.isfile(os.path.join(self.forum_app_dir, 'views.py'))
		
		self.assertTrue(directory_exists, f"{FAILURE_HEADER}The forum app directory does not exist.{FAILURE_FOOTER}")
		self.assertTrue(is_python_package, f"{FAILURE_HEADER}The forum directory is missing files.{FAILURE_FOOTER}")
		self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The forum directory is missing files. {FAILURE_FOOTER}")
	
	def has_urls_module(self):
		module_exists = os.path.isfile(os.path.join(self.forum_app_dir, 'urls.py'))
		self.assertTrue(module_exists, f"{FAILURE_HEADER}The forum app's urls.py module is missing.{FAILURE_FOOTER}")
		

############################################# Admin ###########################################################






############################################# Sighn In \ out ###########################################################

