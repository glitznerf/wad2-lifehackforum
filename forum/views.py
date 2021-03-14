from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

def home(request):
	response = render(request, 'rango/home.html', context=context_dict)
	return response
	
def about(request):
	context_dict = {}
	return render(request, 'forum/about.html', context=context_dict)


