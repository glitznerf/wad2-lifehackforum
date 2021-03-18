from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from forum.models import UserAccount, Category, Hack, Comment

def home(request):
	#for top 3 of week - returns list of length 3 in order
	#hackList = Hack.objects.order_by.['-likes'][:3]


	context_dict = {}
	#context_dict['hacks'] = hackList
	response = render(request, 'forum/home.html', context=context_dict)
	return response
	
	#return HttpResponse("Rango says hey there partner")
	
def about(request):
	context_dict = {}
	return render(request, 'forum/about.html', context=context_dict)

	
def create_category(request):
	context_dict = {}
	response = render(request, 'forum/create_category.html', context=context_dict)
	return response
	
def category(request):
	#categoryList = Category.object
	context_dict = {}
	response = render(request, 'forum/category.html', context=context_dict)
	return response

def hack(request):
	context_dict = {}
	response = render(request, 'forum/hack.html', context=context_dict)
	return response
	
def add_hack(request):
	context_dict = {}
	response = render(request, 'forum/add_hack.html', context=context_dict)
	return response

def all_categories(request):
	context_dict = {}
	response = render(request, 'forum/home.html', context=context_dict)
	return response

def account_info(request):
	context_dict = {}
	response = render(request, 'forum/account_info.html', context=context_dict)
	return response
	
def create_account(request):
	context_dict = {}
	response = render(request, 'forum/create_account.html', context=context_dict)
	return response

def sign_in(request):
	context_dict = {}
	response = render(request, 'forum/sign_in.html', context=context_dict)
	return response


