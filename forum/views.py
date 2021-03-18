from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from forum.models import UserAccount, Category, Hack, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#from rango.forms import CategoryForm, HackForm, RegForm
def home(request):
	#for top 3 of week - returns list of length 3 in order
	#hackList = Hack.objects.order_by.['-likes'][:3]


	context_dict = {}
	#context_dict['hacks'] = hackList
	response = render(request, 'forum/home.html', context=context_dict)
	return response
	
	#return HttpResponse("Rango says hey there partner")
	
def about(request):
	#???????????????????#
	context_dict = {}
	return render(request, 'forum/about.html', context=context_dict)

#@verified_required	
def create_category(request):
	'''
	form = CategoryForm()
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return redirect('/forum/')
		else:
			print(form.errors)
	return render(request, 'rango/add_category.html', {'form': form})
	'''
	
	context_dict = {}
	response = render(request, 'forum/create_category.html', context=context_dict)
	return response
	
def category(request):
	'''
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_categoryName_slug)
		hacks = Hack.objects.filter(categoryName=category)
		context_dict['hacks'] = hacks
		context_dict['category'] = category
		
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
	return render(request, 'forum/category.html', context=context_dict)
	'''
	context_dict = {}
	response = render(request, 'forum/category.html', context=context_dict)
	return response

def hack(request):
	'''
	context_dict = {}
	try:
		hack = Hack.objects.get(slug = hack_hackName_slug)
		comment_list = Comment.objects.filter(hackID = hack)
		context_dict['hack'] = hack
		
	except Hack.DoesNotExist:
		context_dict['hack'] = None
	return render(request, 'forum/hack.html', context=context_dict)
	'''
	
	context_dict = {}
	response = render(request, 'forum/hack.html', context=context_dict)
	return response
	
#@login_required
def add_hack(request):
		'''
	form = HackForm()
	if request.method == 'POST':
		form = HackForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			#perhaps redirect to category not home?
			return redirect('/forum/')
		else:
			print(form.errors)
	return render(request, 'rango/add_hack.html', {'form': form})
	'''
	
	context_dict = {}
	response = render(request, 'forum/add_hack.html', context=context_dict)
	return response

def all_categories(request):
	#search bar not included
	'''
	context_dict = {}
	category_list = Category.objects.order_by('-categoryName')
	context_dict['categries'] = category_list
	response = render(request, 'forum/all_categories.html', context=context_dict)
	return response
	'''
	context_dict = {}
	response = render(request, 'forum/all_categories.html', context=context_dict)
	return response

#@login_required
def account_info(request):
	
	'''
	context_dict = {}
	user_id = UserAccount.objects.get(slug=userAccount_userName_slug)
	hack_list = Hack.objects.filter(userName = user_id)
	context_dict['user'] = user_id
	context_dict['hacks'] = hack_list
	'''
	
	context_dict = {}
	response = render(request, 'forum/account_info.html', context=context_dict)
	return response
	
def create_account(request):
'''
	 # True when registration succeeds.
	 registered = False
	 
	 if request.method == 'POST':

		reg_form = RegForm(requets.POST)

		 if reg_form.is_valid():
			 # Save user form to database.
			 user = reg_form.save()

			 user.set_password(user.password)
			 user.save()

			 registered = True
		 else:
			 # Invalid form print to terminal.
			 print(reg_form.errors)
	 else:
		#re render blank form
		 reg_form = RegForm()
		 
	 # Render the template depending on the context.
	 return render(request, 'forum/register.html', context = {'reg_form': reg_form,'registered': registered})
	'''
	
	context_dict = {}
	response = render(request, 'forum/create_account.html', context=context_dict)
	return response

def sign_in(request):
	'''
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Get username & password from the login form.
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user: #test user returned
			if user.is_active: #test not disabled
				login(request, user) #send login
				return redirect(reverse('forum:home')) #return home
			else:
				#inactive account!
				return HttpResponse("Your Hacks R Us has been disabled")
		else:
			# Bad login details
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("invalid username and/or password")
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'forum/sign_in.html')
	'''
	context_dict = {}
	response = render(request, 'forum/sign_in.html', context=context_dict)
	return response
	
'''
@login_required
def user_logout(request):
	logout(request)
	#user back to the home.
	return redirect(reverse('forum:home'))
'''

